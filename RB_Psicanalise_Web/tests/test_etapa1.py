import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from models import Paciente, Usuario, db


class TestEtapa1(unittest.TestCase):
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

    def login_as(self, email, senha):
        return self.client.post(
            "/login",
            data={"email": email, "senha": senha},
            follow_redirects=True,
        )

    def test_01_rotas_privadas_exigem_login(self):
        resp = self.client.get("/", follow_redirects=False)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login", resp.location)

    def test_02_seed_tres_perfis_e_login(self):
        with self.app.app_context():
            self.assertIsNotNone(Usuario.query.filter_by(perfil="admin_dev").first())
            self.assertIsNotNone(Usuario.query.filter_by(perfil="psicanalista").first())
            self.assertIsNotNone(Usuario.query.filter_by(perfil="atendente").first())

        resp = self.login_as("recepcao@rbpsicanalise.com.br", "Recepcao@RB2026")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Dashboard", resp.data)

    def test_03_crud_paciente_sessao_e_restricao_atendente_anamnese(self):
        # 1. Atendente cadastra paciente
        self.login_as("recepcao@rbpsicanalise.com.br", "Recepcao@RB2026")
        resp = self.client.post(
            "/pacientes/novo",
            data={
                "nome_completo": "Paciente Teste Silva",
                "telefone": "(11) 99999-0000",
                "email": "paciente@teste.com",
                "cpf": "111.222.333-44",
                "termo_aceito": "on",
            },
            follow_redirects=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Paciente Teste Silva", resp.data)

        with self.app.app_context():
            pac = Paciente.query.filter_by(nome_completo="Paciente Teste Silva").first()
            self.assertIsNotNone(pac)
            pid = pac.id

        # 2. Atendente NÃO pode acessar Anamnese nem /admin-dev (403)
        self.assertEqual(self.client.get(f"/paciente/{pid}?aba=anamnese").status_code, 403)
        self.assertEqual(self.client.post(f"/paciente/{pid}/anamnese", data={"motivo_procura": "x"}).status_code, 403)
        self.assertEqual(self.client.get(f"/paciente/{pid}/imprimir/anamnese").status_code, 403)
        self.assertEqual(self.client.get("/admin-dev").status_code, 403)

        # 3. Atendente pode lançar sessão e imprimir cadastro/sessoes
        resp_ses = self.client.post(
            f"/paciente/{pid}/sessao/nova",
            data={
                "data_sessao": "2026-11-26",
                "horario": "14:00",
                "compareceu": "Sim",
                "pagamento": "Pago",
                "valor": "250.00",
                "observacao": "Sessão teste",
            },
            follow_redirects=True,
        )
        self.assertEqual(resp_ses.status_code, 200)
        self.assertIn(b"250.00", resp_ses.data)
        self.assertEqual(self.client.get(f"/paciente/{pid}/imprimir/cadastro").status_code, 200)
        self.assertEqual(self.client.get(f"/paciente/{pid}/imprimir/sessoes").status_code, 200)

        # 4. Psicanalista consegue salvar e imprimir Anamnese
        self.client.post("/logout")
        self.login_as("clinica@rbpsicanalise.com.br", "Clinica@RB2026")
        resp_anam = self.client.post(
            f"/paciente/{pid}/anamnese",
            data={"motivo_procura": "Ansiedade crônica", "historia_familiar": "Pai presente"},
            follow_redirects=True,
        )
        self.assertEqual(resp_anam.status_code, 200)
        self.assertIn(b"Ansiedade", resp_anam.data)
        self.assertEqual(self.client.get(f"/paciente/{pid}/imprimir/anamnese").status_code, 200)

        # 5. Admin Dev acessa /admin-dev e cria usuário
        self.client.post("/logout")
        self.login_as("dev@rbpsicanalise.com.br", "Admin@RB2026")
        resp_adm = self.client.get("/admin-dev")
        self.assertEqual(resp_adm.status_code, 200)
        self.assertIn(b"Backup do Banco", resp_adm.data)


if __name__ == "__main__":
    unittest.main()
