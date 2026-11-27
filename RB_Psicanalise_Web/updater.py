import os
import shutil
import subprocess
import sys
import urllib.request
import json
from datetime import datetime

from version import APP_VERSION, GITHUB_REPO


def _parse_version(v: str):
    v = (v or "0.0.0").lstrip("vV").strip()
    partes = []
    for p in v.split("."):
        digits = "".join(ch for ch in p if ch.isdigit())
        partes.append(int(digits) if digits else 0)
    while len(partes) < 3:
        partes.append(0)
    return tuple(partes[:3])


def versao_mais_nova(remota: str, local: str = APP_VERSION) -> bool:
    return _parse_version(remota) > _parse_version(local)


def verificar_atualizacao(timeout: float = 3.5) -> dict:
    """Consulta a última Release no GitHub sem jamais quebrar o app se estiver offline."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "RB-Psicanalise-Updater",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        tag = data.get("tag_name", "")
        notas = data.get("body", "")
        assets = data.get("assets", [])
        exe_url = ""
        for a in assets:
            if a.get("name", "").lower().endswith(".exe"):
                exe_url = a.get("browser_download_url", "")
                break
        disponivel = bool(tag and versao_mais_nova(tag, APP_VERSION))
        return {
            "ok": True,
            "versao_atual": APP_VERSION,
            "versao_remota": tag.lstrip("vV"),
            "disponivel": disponivel,
            "exe_url": exe_url,
            "notas": notas,
            "release_url": data.get("html_url", ""),
        }
    except Exception as exc:
        return {
            "ok": False,
            "versao_atual": APP_VERSION,
            "disponivel": False,
            "erro": str(exc),
        }


def criar_backup_automatico(db_uri: str, data_dir: str) -> str | None:
    """Cria cópia de segurança do banco SQLite antes de atualizações."""
    if not db_uri.startswith("sqlite:///"):
        return None
    db_path = db_uri.replace("sqlite:///", "", 1)
    if not os.path.exists(db_path):
        return None
    backup_dir = os.path.join(data_dir, "backups")
    os.makedirs(backup_dir, exist_ok=True)
    destino = os.path.join(
        backup_dir,
        f"auto_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
    )
    shutil.copy2(db_path, destino)
    return destino


def aplicar_atualizacao_exe(exe_url: str, db_uri: str, data_dir: str) -> tuple[bool, str]:
    """
    Baixa apenas o novo executável .exe, faz backup do SQLite e agenda
    a substituição in-place após encerrar o processo atual (zero perda de dados).
    """
    if not getattr(sys, "frozen", False):
        return False, "Atualização automática in-place disponível apenas na versão compilada (.exe)."
    if not exe_url:
        return False, "Nenhum arquivo .exe encontrado na Release do GitHub."

    criar_backup_automatico(db_uri, data_dir)

    atual_exe = sys.executable
    novo_exe = atual_exe + ".new"
    bak_exe = atual_exe + ".bak"
    bat_path = os.path.join(os.path.dirname(atual_exe), "_aplicar_atualizacao.bat")

    req = urllib.request.Request(exe_url, headers={"User-Agent": "RB-Psicanalise-Updater"})
    with urllib.request.urlopen(req, timeout=60) as resp, open(novo_exe, "wb") as out:
        shutil.copyfileobj(resp, out)

    pid = os.getpid()
    bat_content = f"""@echo off
set "_MEIPASS2="
set "_PYI_ARCHIVE_FILE="
set "PYTHONHOME="
set "PYTHONPATH="
timeout /t 2 /nobreak >nul
taskkill /F /PID {pid} >nul 2>&1
timeout /t 1 /nobreak >nul
if exist "{bak_exe}" del /f /q "{bak_exe}"
move /y "{atual_exe}" "{bak_exe}" >nul
move /y "{novo_exe}" "{atual_exe}" >nul
explorer.exe "{atual_exe}"
del "%~f0"
"""
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(bat_content)

    clean_env = os.environ.copy()
    for k in ("_MEIPASS2", "_PYI_ARCHIVE_FILE", "PYTHONHOME", "PYTHONPATH"):
        clean_env.pop(k, None)

    subprocess.Popen(
        ["cmd", "/c", bat_path],
        env=clean_env,
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW,
        close_fds=True,
    )
    return True, "Atualização baixada! O aplicativo será reiniciado na nova versão em instantes."
