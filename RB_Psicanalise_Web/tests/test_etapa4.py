import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from models import db
from updater import criar_backup_automatico, verificar_atualizacao, versao_mais_nova


class TestEtapa4(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        self.backup_dir = tempfile.mkdtemp()
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
            data={"email": "dev@rbpsicanalise.com.br", "senha": "Admin@RB2026"},
        )

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.engine.dispose()
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_01_comparacao_de_versoes(self):
        self.assertTrue(versao_mais_nova("v1.1.0", "1.0.0"))
        self.assertTrue(versao_mais_nova("2.0.0", "1.9.9"))
        self.assertFalse(versao_mais_nova("v1.0.0", "1.0.0"))
        self.assertFalse(versao_mais_nova("0.9.5", "1.0.0"))

    def test_02_backup_automatico_antes_de_atualizar(self):
        caminho = criar_backup_automatico(f"sqlite:///{self.db_path}", self.backup_dir)
        self.assertIsNotNone(caminho)
        self.assertTrue(os.path.exists(caminho))

    def test_03_checar_atualizacao_offline_nao_quebra(self):
        with patch("updater.urllib.request.urlopen", side_effect=OSError("Sem internet")):
            res = verificar_atualizacao()
            self.assertFalse(res["ok"])
            self.assertFalse(res["disponivel"])

        r_api = self.client.get("/api/sistema/checar-atualizacao")
        self.assertEqual(r_api.status_code, 200)
        self.assertIn("versao_atual", r_api.get_json())


if __name__ == "__main__":
    unittest.main()
