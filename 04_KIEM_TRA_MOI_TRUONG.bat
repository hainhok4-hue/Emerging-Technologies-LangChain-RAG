@echo off
cd /d "%~dp0"
chcp 65001 >nul
echo ===== PYTHON =====
where python
python --version
echo ===== OLLAMA =====
where ollama
ollama --version
ollama list
echo ===== CAC FILE PDF =====
dir /b "data\pdfs\*.pdf"
echo ===== MOI TRUONG =====
if exist ".venv\Scripts\python.exe" ".venv\Scripts\python.exe" -m pip --version
pause
