import os
import shutil
import socket
import subprocess
import sys
import threading
import time
import webbrowser

import pystray
from PIL import Image
from waitress import serve

from app import app
from config import DATA_DIR, RESOURCE_DIR
from updater import criar_backup_automatico

APP_URL = "http://127.0.0.1:5000"


def servidor_ja_ativo(host="127.0.0.1", port=5000) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def garantir_atalho_area_de_trabalho():
    """
    No modo .exe, copia o executável para %LOCALAPPDATA%/RB_Psicanalise/App
    e cria o atalho 'RB Psicanálise' na Área de Trabalho com o ícone da clínica.
    """
    if not getattr(sys, "frozen", False):
        return

    try:
        app_dir = os.path.join(DATA_DIR, "App")
        os.makedirs(app_dir, exist_ok=True)
        destino_exe = os.path.join(app_dir, "RB_Psicanalise.exe")
        atual_exe = os.path.abspath(sys.executable)

        # Copia o .exe para a pasta fixa se estiver rodando de Downloads/outra pasta
        if os.path.normcase(atual_exe) != os.path.normcase(destino_exe):
            try:
                shutil.copy2(atual_exe, destino_exe)
            except Exception:
                destino_exe = atual_exe

        icone_src = os.path.join(RESOURCE_DIR, "static", "app_icon.ico")
        icone_dst = os.path.join(app_dir, "app_icon.ico")
        if os.path.exists(icone_src):
            shutil.copy2(icone_src, icone_dst)

        ps_cmd = (
            f"$desktop = [Environment]::GetFolderPath('Desktop'); "
            f"$lnk = Join-Path $desktop 'RB Psicanálise.lnk'; "
            f"$ws = New-Object -ComObject WScript.Shell; "
            f"$s = $ws.CreateShortcut($lnk); "
            f"$s.TargetPath = '{destino_exe}'; "
            f"$s.WorkingDirectory = '{app_dir}'; "
            f"$s.IconLocation = '{icone_dst}'; "
            f"$s.Description = 'RB Psicanálise — Sistema Clínico'; "
            f"$s.Save()"
        )
        subprocess.run(
            ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps_cmd],
            creationflags=subprocess.CREATE_NO_WINDOW,
            timeout=8,
        )
    except Exception:
        pass


def abrir_navegador():
    time.sleep(1.2)
    webbrowser.open(APP_URL)


def iniciar_bandeja():
    icone_png = os.path.join(RESOURCE_DIR, "static", "app_icon.png")
    img = Image.open(icone_png) if os.path.exists(icone_png) else Image.new("RGB", (64, 64), (15, 23, 42))

    def acao_abrir(icon, item):
        webbrowser.open(APP_URL)

    def acao_pasta(icon, item):
        os.startfile(DATA_DIR)

    def acao_sair(icon, item):
        icon.stop()
        os._exit(0)

    menu = pystray.Menu(
        pystray.MenuItem("Abrir RB Psicanálise", acao_abrir, default=True),
        pystray.MenuItem("Pasta de Dados e Backups", acao_pasta),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Encerrar Sistema", acao_sair),
    )
    tray = pystray.Icon("RB_Psicanalise", img, "RB Psicanálise — Sistema Clínico", menu)
    tray.run()


if __name__ == "__main__":
    # Se já estiver aberto em segundo plano, apenas abre a aba do navegador
    if servidor_ja_ativo():
        webbrowser.open(APP_URL)
        sys.exit(0)

    garantir_atalho_area_de_trabalho()
    criar_backup_automatico(app.config["SQLALCHEMY_DATABASE_URI"], DATA_DIR)

    threading.Thread(
        target=lambda: serve(app, host="127.0.0.1", port=5000, threads=4),
        daemon=True,
    ).start()
    threading.Thread(target=abrir_navegador, daemon=True).start()

    iniciar_bandeja()
