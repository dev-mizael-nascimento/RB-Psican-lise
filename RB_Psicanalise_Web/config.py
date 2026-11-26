import os
import sys
from dotenv import load_dotenv


def get_base_dir():
    """Retorna o diretório do código ou do executável."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.dirname(__file__))


def get_data_dir():
    """
    No modo .exe (frozen), grava banco SQLite, .env e backups em %LOCALAPPDATA%/RB_Psicanalise
    para que atualizações do executável jamais afetem ou percam dados do cliente.
    """
    if getattr(sys, "frozen", False):
        local_app = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
        data_dir = os.path.join(local_app, "RB_Psicanalise")
        os.makedirs(data_dir, exist_ok=True)
        return data_dir
    return get_base_dir()


def get_resource_dir():
    """Retorna o diretório de templates/estáticos (compatível com PyInstaller _MEIPASS)."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.abspath(os.path.dirname(__file__))


BASE_DIR = get_base_dir()
DATA_DIR = get_data_dir()
RESOURCE_DIR = get_resource_dir()

# Carrega .env da pasta de dados (persistente) ou da pasta base
env_data = os.path.join(DATA_DIR, ".env")
env_base = os.path.join(BASE_DIR, ".env")
load_dotenv(env_data if os.path.exists(env_data) else env_base)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "rb-psicanalise-secret-key-local-2026")
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")

    _raw_db_url = os.environ.get("DATABASE_URL", "sqlite:///rb_psicanalise.db")
    if _raw_db_url.startswith("postgres://"):
        _raw_db_url = _raw_db_url.replace("postgres://", "postgresql://", 1)
    elif _raw_db_url.startswith("sqlite:///") and not os.path.isabs(_raw_db_url.replace("sqlite:///", "", 1)):
        db_rel = _raw_db_url.replace("sqlite:///", "", 1)
        _raw_db_url = f"sqlite:///{os.path.join(DATA_DIR, db_rel)}"

    SQLALCHEMY_DATABASE_URI = _raw_db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APP_BASE_URL = os.environ.get("APP_BASE_URL", "http://127.0.0.1:5000").rstrip("/")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = FLASK_ENV == "production" and APP_BASE_URL.startswith("https://")
    WTF_CSRF_ENABLED = True
