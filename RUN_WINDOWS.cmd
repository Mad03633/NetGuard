@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Create an environment first: python -m venv .venv
  echo Then install: .venv\Scripts\python.exe -m pip install -r requirements.txt
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m streamlit run streamlit_app.py --server.address 127.0.0.1
