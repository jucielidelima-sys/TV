@echo off
cd /d %~dp0
echo Instalando/validando Streamlit...
python -m pip install -r requirements.txt
echo Abrindo painel em modo TV...
python -m streamlit run app.py --server.address localhost --server.port 8501 --browser.gatherUsageStats false
pause
