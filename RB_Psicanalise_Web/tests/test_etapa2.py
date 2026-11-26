import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from models import Agendamento, KanbanColuna, Paciente, db


class TestEtapa2(unittest.TestCase):
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

    def test_01_kanban_colunas_card_rapido_e_mover(self):
        # 1. Criar nova coluna
        r_col = self.client.post("/api/kanban/colunas", json={"titulo": "Lista de Espera", "cor": "#059669"})
        self.assertEqual(r_col.status_code, 200)
        col_id = r_col.get_json()["coluna"]["id"]

        # 2. Renomear coluna
        r_ed = self.client.post(f"/api/kanban/colunas/{col_id}/editar", json={"titulo": "Espera VIP"})
        self.assertEqual(r_ed.status_code, 200)

        # 3. Card rápido na primeira coluna
        with self.app.app_context():
            col1 = KanbanColuna.query.order_by(KanbanColuna.ordem.asc()).first()
            col1_id = col1.id

        r_card = self.client.post(
            "/api/kanban/card-rapido",
            json={"nome_completo": "Carlos Kanban", "telefone": "(11) 98888-7777", "coluna_id": col1_id},
        )
        self.assertEqual(r_card.status_code, 200)
        pac_id = r_card.get_json()["paciente_id"]

        # 4. Mover card para a nova coluna
        r_mov = self.client.post(
            "/api/kanban/mover",
            json={"paciente_id": pac_id, "coluna_id": col_id, "ordem_ids": [pac_id]},
        )
        self.assertEqual(r_mov.status_code, 200)

        with self.app.app_context():
            p = db.session.get(Paciente, pac_id)
            self.assertEqual(p.kanban_coluna_id, col_id)

        # 5. Excluir coluna move o paciente para a primeira coluna disponível
        r_del = self.client.post(f"/api/kanban/colunas/{col_id}/excluir")
        self.assertEqual(r_del.status_code, 200)
        with self.app.app_context():
            p = db.session.get(Paciente, pac_id)
            self.assertNotEqual(p.kanban_coluna_id, col_id)

        # 6. Página Kanban renderiza normalmente
        self.assertEqual(self.client.get("/kanban").status_code, 200)

    def test_02_agenda_visual_crud_e_integracao_sessoes(self):
        r_card = self.client.post(
            "/api/kanban/card-rapido",
            json={"nome_completo": "Ana Agenda", "telefone": "(11) 97777-6666"},
        )
        pac_id = r_card.get_json()["paciente_id"]

        # 1. Criar agendamento
        r_ag = self.client.post(
            "/api/agendamentos",
            json={
                "paciente_id": pac_id,
                "inicio": "2026-11-27T15:00",
                "fim": "2026-11-27T15:50",
                "modalidade": "Online",
                "valor": "300.00",
                "pagamento": "Pendente",
                "observacao": "Primeira entrevista",
            },
        )
        self.assertEqual(r_ag.status_code, 200)
        ag_id = r_ag.get_json()["id"]

        # 2. Listar eventos JSON para FullCalendar
        r_list = self.client.get("/api/agendamentos")
        self.assertEqual(r_list.status_code, 200)
        eventos = r_list.get_json()
        self.assertEqual(len(eventos), 1)
        self.assertIn("Ana Agenda", eventos[0]["title"])

        # 3. Atualizar comparecimento + pagamento (reflete no Controle de Sessões)
        r_upd = self.client.post(
            f"/api/agendamentos/{ag_id}/atualizar",
            json={"compareceu": "Sim", "pagamento": "Pago", "inicio": "2026-11-28T16:00"},
        )
        self.assertEqual(r_upd.status_code, 200)

        with self.app.app_context():
            ag = db.session.get(Agendamento, ag_id)
            self.assertEqual(ag.compareceu, "Sim")
            self.assertEqual(ag.pagamento, "Pago")
            self.assertEqual(ag.status, "Realizado")
            self.assertEqual(ag.inicio.strftime("%Y-%m-%d %H:%M"), "2026-11-28 16:00")

        # 4. Página Agenda renderiza
        self.assertEqual(self.client.get("/agenda").status_code, 200)

        # 5. Excluir agendamento
        r_del = self.client.post(f"/api/agendamentos/{ag_id}/excluir")
        self.assertEqual(r_del.status_code, 200)


if __name__ == "__main__":
    unittest.main()
