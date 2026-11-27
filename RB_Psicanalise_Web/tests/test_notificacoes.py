import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from models import db


class TestNotificacoes(unittest.TestCase):
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

    def test_01_central_notificacoes_lembretes_whatsapp(self):
        # 1. Configura WhatsApp do Psicanalista
        self.client.post("/login", data={"email": "dev@rbpsicanalise.com.br", "senha": "Admin@RB2026"})
        self.client.post(
            "/admin-dev",
            data={
                "acao": "salvar_configs",
                "app_base_url": "http://127.0.0.1:5000",
                "whatsapp_psicanalista": "(11) 98888-1111",
                "whatsapp_atendimento": "(11) 97777-2222",
            },
        )
        self.client.post("/logout")

        # 2. Atendente cria paciente e agenda sessão para hoje
        self.client.post("/login", data={"email": "recepcao@rbpsicanalise.com.br", "senha": "Recepcao@RB2026"})
        r_pac = self.client.post(
            "/api/kanban/card-rapido",
            json={"nome_completo": "Marcos Lembrete", "telefone": "(11) 96666-3333"},
        )
        pid = r_pac.get_json()["paciente_id"]

        agora = datetime.now() + timedelta(hours=2)
        r_ag = self.client.post(
            "/api/agendamentos",
            json={
                "paciente_id": pid,
                "inicio": agora.strftime("%Y-%m-%dT%H:%M"),
                "modalidade": "Presencial",
                "valor": "250.00",
            },
        )
        ag_id = r_ag.get_json()["id"]

        # 3. Acessa Central de Notificações e valida botões WhatsApp do paciente e do psicanalista
        r_not = self.client.get("/notificacoes")
        self.assertEqual(r_not.status_code, 200)
        self.assertIn(b"Marcos Lembrete", r_not.data)
        self.assertIn(b"https://wa.me/5511966663333", r_not.data)
        self.assertIn(b"https://wa.me/5511988881111", r_not.data)

        # 4. Marca lembrete como enviado
        r_mark = self.client.post(f"/api/notificacoes/marcar-lembrete/{ag_id}")
        self.assertEqual(r_mark.status_code, 200)
        self.assertTrue(r_mark.get_json()["lembrete_enviado"])


if __name__ == "__main__":
    unittest.main()
