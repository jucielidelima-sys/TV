import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Painel TV", layout="wide", initial_sidebar_state="collapsed")

APP_URL = "https://painel-apputivo-2ze4gkolje3kt8orpk4laa.streamlit.app/?tv=1&modo=tv&embed=true"
SLIDE_SECONDS = 10
APP_SECONDS = 30

st.markdown("""
<style>
html, body, [data-testid=\"stAppViewContainer\"], [data-testid=\"stApp\"] {background:#000; margin:0; padding:0; overflow:hidden;}
[data-testid=\"stHeader\"], [data-testid=\"stToolbar\"], [data-testid=\"stDecoration\"], footer {display:none !important;}
.block-container {padding:0 !important; margin:0 !important; max-width:100% !important;}
</style>
""", unsafe_allow_html=True)

def img_to_b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")

slides_dir = Path(__file__).parent / "slides"
slide_files = sorted(slides_dir.glob("*.png"), key=lambda p: int(''.join(filter(str.isdigit, p.stem)) or 0))
slides = [f"data:image/png;base64,{img_to_b64(p)}" for p in slide_files]

if not slides:
    st.error("Nenhum slide encontrado na pasta slides.")
    st.stop()

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<style>
html, body {{ margin:0; padding:0; width:100%; height:100%; background:#000; overflow:hidden; }}
#wrap {{ position:fixed; inset:0; width:100vw; height:100vh; background:#000; }}
#slide {{ width:100vw; height:100vh; object-fit:contain; background:#000; display:block; }}
#appframe {{ width:100vw; height:100vh; border:0; display:none; background:#fff; }}
#label {{ position:fixed; top:8px; left:12px; z-index:9999; color:white; font-family:Arial, sans-serif; font-size:14px; background:rgba(0,0,0,.45); padding:6px 10px; border-radius:6px; }}
</style>
</head>
<body>
<div id='wrap'>
  <img id='slide' />
  <iframe id='appframe' allow='fullscreen' src='about:blank'></iframe>
  <div id='label'></div>
</div>
<script>
const slides = {slides!r};
const appUrl = {APP_URL!r};
const slideMs = {SLIDE_SECONDS * 1000};
const appMs = {APP_SECONDS * 1000};
let i = 0;
const img = document.getElementById('slide');
const frame = document.getElementById('appframe');
const label = document.getElementById('label');

function showSlide() {{
  frame.style.display = 'none';
  img.style.display = 'block';
  img.src = slides[i];
  label.textContent = 'Slide ' + (i+1) + ' • 10 segundos';
  i++;
  if (i >= slides.length) {{
    i = 0;
    setTimeout(showApp, slideMs);
  }} else {{
    setTimeout(showSlide, slideMs);
  }}
}}

function showApp() {{
  img.style.display = 'none';
  frame.style.display = 'block';
  label.textContent = 'Painel Apputivo • Modo TV • 30 segundos';
  frame.src = appUrl + '&_=' + Date.now();
  setTimeout(showSlide, appMs);
}}

showSlide();
</script>
</body>
</html>
"""

components.html(html, height=1080, scrolling=False)
