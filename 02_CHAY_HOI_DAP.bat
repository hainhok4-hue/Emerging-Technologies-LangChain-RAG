@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul
set "PYTHONUTF8=1"
title HOI DAP PDF LANGCHAIN
if not exist ".venv\Scripts\python.exe" (
    echo [LOI] Ban can chay 01_CAI_DAT_LAN_DAU.bat truoc.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" app.py
set "status=%errorlevel%"
echo.
if not "%status%"=="0" echo [LOI] Chuong trinh bao loi. Doc thong bao phia tren.
pause
exit /b %status%
