@echo off
title RB Psicanalise - Sistema Clinico
echo Iniciando Sistema Web RB Psicanalise...
cd /d "%~dp0"
start "" http://127.0.0.1:5000
python app.py
pause
