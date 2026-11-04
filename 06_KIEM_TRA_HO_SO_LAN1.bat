@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul
set "PYTHONUTF8=1"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" "scripts\check_lan1.py" --after-run
) else (
  python "scripts\check_lan1.py"
)
pause
