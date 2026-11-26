import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from models import Formulario, FormularioEnvio, db


class TestEtapa3(unittest.TestCase):
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
        self.client.post(
            "/login",
            data={"email": "recepcao@rbpsicanalise.com.br", "senha": "Recepcao@RB2026"},
            follow_redirects=True,
        )

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.engine.dispose()
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_01_modelos_prontos_e_form_builder(self):
        with self.app.app_context():
            self.assertGreaterEqual(Formulario.query.count(), 2)

        r_page = self.client.get("/formularios")
        self.assertEqual(r_page.status_code, 200)

        # Criar formulário customizado
        r_save = self.client.post(
            "/api/formularios/salvar",
            json={
                "titulo": "Triagem Express",
                "descricao": "Teste",
                "campos": [
                    {"id": "c1", "label": "Como se sente hoje?", "tipo": "texto", "obrigatorio": True, "opcoes": []},
                    {"id": "c2", "label": "Aceita atendimento online?", "tipo": "sim_nao", "obrigatorio": True, "opcoes": []},
                ],
            },
        )
        self.assertEqual(r_save.status_code, 200)
        form_id = r_save.get_json()["id"]

        # Criar paciente e gerar link público
        r_pac = self.client.post(
            "/api/kanban/card-rapido",
            json={"nome_completo": "Beatriz Form", "telefone": "(11) 91234-5678"},
        )
        pac_id = r_pac.get_json()["paciente_id"]

        r_link = self.client.post(
            "/api/formularios/gerar-link",
            json={"formulario_id": form_id, "paciente_id": pac_id},
        )
        self.assertEqual(r_link.status_code, 200)
        dados_link = r_link.get_json()
        token = dados_link["token"]
        self.assertIn(f"/responder/{token}", dados_link["url"])
        self.assertIn("https://wa.me/5511912345678", dados_link["whatsapp_url"])

        # Simular paciente sem login (logout primeiro!)
        self.client.post("/logout")

        # Token inválido -> 404
        self.assertEqual(self.client.get("/responder/token-invalido-123").status_code, 404)

        # Paciente abre o link público sem login
        r_pub = self.client.get(f"/responder/{token}")
        self.assertEqual(r_pub.status_code, 200)
        self.assertIn(b"Beatriz Form", r_pub.data)

        # Paciente envia respostas
        r_sub = self.client.post(
            f"/responder/{token}",
            data={"c1": "Ansiosa mas motivada", "c2": "Sim"},
        )
        self.assertEqual(r_sub.status_code, 200)
        self.assertIn(b"Respostas recebidas com sucesso", r_sub.data)

        with self.app.app_context():
            env = FormularioEnvio.query.filter_by(token=token).first()
            self.assertEqual(env.status, "Respondido")
            self.assertEqual(env.respostas.get("Como se sente hoje?"), "Ansiosa mas motivada")

        # Reabertura do mesmo link mostra confirmação e não permite reenviar
        r_dup = self.client.post(f"/responder/{token}", data={"c1": "Tentativa", "c2": "Não"})
        self.assertEqual(r_dup.status_code, 200)
        with self.app.app_context():
            env = FormularioEnvio.query.filter_by(token=token).first()
            self.assertEqual(env.respostas.get("Como se sente hoje?"), "Ansiosa mas motivada")

        # Verificar no prontuário logado
        self.client.post(
            "/login",
            data={"email": "recepcao@rbpsicanalise.com.br", "senha": "Recepcao@RB2026"},
        )
        r_pront = self.client.get(f"/paciente/{pac_id}?aba=formularios")
        self.assertEqual(r_pront.status_code, 200)
        self.assertIn(b"Ansiosa mas motivada", r_pront.data)

    def test_02_roteamento_whatsapp_e_sigilo_anamnese(self):
        # 1. Admin Dev configura números de WhatsApp separados
        self.client.post("/logout")
        self.client.post(
            "/login",
            data={"email": "dev@rbpsicanalise.com.br", "senha": "Admin@RB2026"},
        )
        r_cfg = self.client.post(
            "/admin-dev",
            data={
                "acao": "salvar_configs",
                "app_base_url": "http://127.0.0.1:5000",
                "whatsapp_psicanalista": "(11) 91111-1111",
                "whatsapp_atendimento": "(11) 92222-2222",
            },
            follow_redirects=True,
        )
        self.assertEqual(r_cfg.status_code, 200)

        # 2. Cria paciente e envia Anamnese (sigiloso=True)
        r_pac = self.client.post(
            "/api/kanban/card-rapido",
            json={"nome_completo": "Lucas Sigilo", "telefone": "(11) 93333-3333"},
        )
        pac_id = r_pac.get_json()["paciente_id"]

        with self.app.app_context():
            form_anam = Formulario.query.filter_by(sigiloso=True).first()
            self.assertIsNotNone(form_anam)
            fid_anam = form_anam.id

        r_link = self.client.post(
            "/api/formularios/gerar-link",
            json={"formulario_id": fid_anam, "paciente_id": pac_id},
        )
        token = r_link.get_json()["token"]

        # 3. Paciente responde sem login -> botão WhatsApp deve ir para o Psicanalista (91111-1111)
        self.client.post("/logout")
        r_sub = self.client.post(
            f"/responder/{token}",
            data={"motivo": "Segredo clínico profundo"},
        )
        self.assertEqual(r_sub.status_code, 200)
        self.assertIn(b"https://wa.me/5511911111111", r_sub.data)

        # 4. Atendente NÃO vê a resposta sigilosa no prontuário nem na tela de formulários
        self.client.post(
            "/login",
            data={"email": "recepcao@rbpsicanalise.com.br", "senha": "Recepcao@RB2026"},
        )
        r_atend = self.client.get(f"/paciente/{pac_id}?aba=formularios")
        self.assertNotIn(b"Segredo", r_atend.data)
        self.assertIn(b"Respostas sigilosas", r_atend.data)

        # 5. Psicanalista VÊ a resposta sigilosa
        self.client.post("/logout")
        self.client.post(
            "/login",
            data={"email": "clinica@rbpsicanalise.com.br", "senha": "Clinica@RB2026"},
        )
        r_psi = self.client.get(f"/paciente/{pac_id}?aba=formularios")
        self.assertIn(b"Segredo", r_psi.data)


if __name__ == "__main__":
    unittest.main()
