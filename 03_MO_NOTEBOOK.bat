@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul
set "PYTHONUTF8=1"
title NOTEBOOK LANGCHAIN
if not exist ".venv\Scripts\python.exe" (
    echo [LOI] Chay 01_CAI_DAT_LAN_DAU.bat truoc.
    pause
    exit /b 1
)
echo Dang cai / kiem tra JupyterLab...
".venv\Scripts\python.exe" -m pip install -r requirements-notebook.txt
if errorlevel 1 (
    echo [LOI] Khong cai duoc JupyterLab.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" -m jupyter lab "notebooks\DEMO_TUNG_HAM.ipynb"
pause
