@echo off
cd /d %~dp0

echo Instalando dependencias...
python -m pip install -r requirements.txt

echo Instalando navegador interno do Playwright...
python -m playwright install chromium

echo Abrindo painel TV...
python -m streamlit run app.py --server.address localhost --server.port 8501
pause
