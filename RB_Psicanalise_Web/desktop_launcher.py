import threading
import time
import webbrowser

from waitress import serve
from app import app
from config import DATA_DIR
from updater import criar_backup_automatico


def abrir_navegador():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    # Garante backup preventivo a cada inicialização do .exe
    criar_backup_automatico(app.config["SQLALCHEMY_DATABASE_URI"], DATA_DIR)
    threading.Thread(target=abrir_navegador, daemon=True).start()
    serve(app, host="127.0.0.1", port=5000, threads=4)
