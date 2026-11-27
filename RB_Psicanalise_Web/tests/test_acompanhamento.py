import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from models import EvolucaoClinica, db


class TestAcompanhamentoClinico(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        self.app = create_app(
            {
                "TESTING": True,
                "WTF_CSRF_ENABLED": False,
                "SQLALCHEMY_DATABASE_URI": f"sqlite:///{self.db_path}",
            }
        )
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.engine.dispose()
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_01_acompanhamento_sigilo_atendente_e_evolucao_continua(self):
        # 1. Atendente cria paciente, mas NÃO pode acessar Acompanhamento Clínico (403)
        self.client.post("/login", data={"email": "recepcao@rbpsicanalise.com.br", "senha": "Recepcao@RB2026"})
        r_pac = self.client.post(
            "/api/kanban/card-rapido",
            json={"nome_completo": "Helena Evolução", "telefone": "(11) 95555-4444"},
        )
        pid = r_pac.get_json()["paciente_id"]

        self.assertEqual(self.client.get(f"/paciente/{pid}?aba=acompanhamento").status_code, 403)
        self.assertEqual(
            self.client.post(f"/paciente/{pid}/acompanhamento/nova", data={"anotacoes_clinicas": "x"}).status_code,
            403,
        )
        self.assertEqual(self.client.get(f"/paciente/{pid}/imprimir/acompanhamento").status_code, 403)

        # 2. Psicanalista registra múltiplas sessões na mesma ficha e imprime tudo junto
        self.client.post("/logout")
        self.client.post("/login", data={"email": "clinica@rbpsicanalise.com.br", "senha": "Clinica@RB2026"})

        self.client.post(
            f"/paciente/{pid}/acompanhamento/nova",
            data={
                "numero_sessao": "1",
                "data_sessao": "20/11/2026",
                "tema_central": "Demanda inicial e luto",
                "anotacoes_clinicas": "Paciente trouxe relato intenso sobre perda recente.",
                "intervencoes": "Escuta acolhedora e pontuação sobre culpa.",
            },
        )
        r_s2 = self.client.post(
            f"/paciente/{pid}/acompanhamento/nova",
            data={
                "numero_sessao": "2",
                "data_sessao": "26/11/2026",
                "tema_central": "Sonho repetitivo",
                "anotacoes_clinicas": "Associou o sonho à infância e relação paterna.",
                "intervencoes": "Retomar significantes na próxima sessão.",
            },
            follow_redirects=True,
        )
        self.assertEqual(r_s2.status_code, 200)
        self.assertIn(b"Demanda inicial e luto", r_s2.data)
        self.assertIn(b"Sonho repetitivo", r_s2.data)

        with self.app.app_context():
            evs = EvolucaoClinica.query.filter_by(paciente_id=pid).order_by(EvolucaoClinica.numero_sessao.asc()).all()
            self.assertEqual(len(evs), 2)
            ev1_id = evs[0].id

        # 3. Editar Sessão 1
        self.client.post(
            f"/paciente/{pid}/acompanhamento/{ev1_id}/editar",
            data={
                "data_sessao": "20/11/2026",
                "tema_central": "Demanda inicial e luto (revisado)",
                "anotacoes_clinicas": "Anotação revisada pelo psicanalista.",
                "intervencoes": "Pontuação mantida.",
            },
        )

        # 4. Impressão A4 unificada traz todas as sessões juntas
        r_imp = self.client.get(f"/paciente/{pid}/imprimir/acompanhamento")
        self.assertEqual(r_imp.status_code, 200)
        self.assertIn(b"Demanda inicial e luto (revisado)", r_imp.data)
        self.assertIn(b"Sonho repetitivo", r_imp.data)


if __name__ == "__main__":
    unittest.main()
