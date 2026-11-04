@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul
set "PYTHONUTF8=1"
set "VENV_PY=.venv\Scripts\python.exe"
if not exist "%VENV_PY%" (
  echo [ERROR] Run 01_CAI_DAT_LAN_DAU.bat first.
  pause
  exit /b 1
)
echo [1/5] Installing notebook and test helpers...
"%VENV_PY%" -m pip install -r requirements-notebook.txt
if errorlevel 1 goto fail
echo [2/5] Checking Ollama and Qwen model...
"%VENV_PY%" -c "from app import check_ollama; check_ollama()"
if errorlevel 1 goto fail
echo [3/5] Executing ALL notebook cells; actual outputs will be saved...
"%VENV_PY%" -m jupyter nbconvert --to notebook --execute "notebooks\DEMO_TUNG_HAM.ipynb" --ExecutePreprocessor.timeout=1800 --ExecutePreprocessor.kernel_name=python3 --output "DEMO_TUNG_HAM_DA_CHAY.ipynb" --output-dir "notebooks"
if errorlevel 1 goto fail
echo [4/5] Running actual Python tests...
"%VENV_PY%" -m pytest tests\test_contracts.py -q > "ket_qua\pytest_ket_qua.txt" 2>&1
if errorlevel 1 (
  echo [WARNING] Pytest found a problem; inspect ket_qua\pytest_ket_qua.txt
  type "ket_qua\pytest_ket_qua.txt"
)
echo [5/5] Checking the complete submission...
"%VENV_PY%" "scripts\check_lan1.py" --after-run
if errorlevel 1 goto fail
echo.
echo [DONE] Actual evidence is in notebooks\DEMO_TUNG_HAM_DA_CHAY.ipynb and ket_qua\ket_qua_5_cau_hinh.csv
echo [REMINDER] Results are specific to your Windows machine. Do not call one sample a full benchmark.
pause
exit /b 0
:fail
echo [NOT COMPLETE] The program did not create reliable full-run evidence. Read the error above.
pause
exit /b 1
