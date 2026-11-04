@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul
set "PYTHONUTF8=1"
title CAI DAT LANGCHAIN PDF QA

echo === CAI DAT LAN DAU - LANGCHAIN PDF QA ===
if exist ".venv\Scripts\python.exe" goto install_packages
where py >nul 2>nul
if not errorlevel 1 (
    py -3.11 -m venv .venv 2>nul
    if exist ".venv\Scripts\python.exe" goto install_packages
    py -3.12 -m venv .venv 2>nul
    if exist ".venv\Scripts\python.exe" goto install_packages
    py -3 -m venv .venv
) else (
    where python >nul 2>nul
    if errorlevel 1 (
        echo [LOI] Chua cai Python. Cai Python 3.11 64-bit truoc.
        goto fail
    )
    python -m venv .venv
)
if not exist ".venv\Scripts\python.exe" (
    echo [LOI] Khong tao duoc moi truong .venv.
    goto fail
)
:install_packages
echo [1/3] Dang cai thu vien Python...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto fail
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto fail

echo [2/3] Kiem tra Ollama...
where ollama >nul 2>nul
if errorlevel 1 (
    echo [LOI] Chua cai Ollama. Vao https://ollama.com/download/windows
    echo Cai Ollama, dong mo lai CMD, sau do chay lai file BAT nay.
    goto fail
)

echo [3/3] Dang tai model Qwen2.5:3b (khoang 1.9 GB)...
ollama pull qwen2.5:3b
if errorlevel 1 goto fail

echo.
echo [OK] DA CAI DAT XONG!
echo Lan sau: nhap 02_CHAY_HOI_DAP.bat hoac nhap dup chuot file.
pause
exit /b 0
:fail
echo.
echo [LOI] Cai dat chua thanh cong. Xem thong bao ngay phia tren.
pause
exit /b 1
