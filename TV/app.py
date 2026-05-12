import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="TV - Slides + Painel", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"], header, footer, #MainMenu {display:none!important;}
.block-container {padding:0!important; margin:0!important; max-width:100%!important;}
html, body, [data-testid="stAppViewContainer"], .main {background:#000!important; overflow:hidden!important;}
iframe {display:block!important;}
</style>
""", unsafe_allow_html=True)

BASE = Path(__file__).parent
SLIDES_DIR = BASE / "slides"
slides = sorted(SLIDES_DIR.glob("*.png"))

if not slides:
    st.error("Nenhum slide encontrado na pasta 'slides'.")
    st.stop()

def img_to_data_uri(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("utf-8")

slide_uris = [img_to_data_uri(p) for p in slides]
js_slides = ",\n".join([repr(s) for s in slide_uris])

# Vários parâmetros para aumentar a chance do painel abrir em MODO TV, caso o app reconheça algum deles.
PANEL_URL = "https://painel-apputivo-2ze4gkolje3kt8orpk4laa.streamlit.app/?tv=1&modo=tv&mode=tv&layout=tv&view=tv&desktop=1"

html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<style>
  html, body {{ margin:0; padding:0; background:#000; width:100vw; height:100vh; overflow:hidden; }}
  #stage {{ position:fixed; inset:0; background:#000; overflow:hidden; }}
  .slide {{ width:100vw; height:100vh; object-fit:contain; background:#000; display:block; }}
  #panelWrap {{ width:100vw; height:100vh; overflow:hidden; background:#000; display:flex; justify-content:center; align-items:flex-start; }}
  /* O iframe abaixo é propositalmente grande. Isso força o app externo a enxergar uma tela larga/TV,
     evitando que ele assuma layout de celular por causa do tamanho do iframe. */
  #panelFrame {{ width:1920px; height:1080px; border:0; transform-origin: top center; background:#000; }}
  #label {{ position:fixed; top:8px; left:10px; z-index:10; color:white; font:14px Arial; background:rgba(0,0,0,.45); padding:4px 8px; border-radius:6px; }}
</style>
</head>
<body>
<div id="stage"></div>
<div id="label"></div>
<script>
const slides = [{js_slides}];
const panelUrl = "{PANEL_URL}";
let index = 0;
let showingPanel = false;
const stage = document.getElementById('stage');
const label = document.getElementById('label');

function scalePanel() {{
  const f = document.getElementById('panelFrame');
  if (!f) return;
  const scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
  f.style.transform = `scale(${{scale}})`;
}}
window.addEventListener('resize', scalePanel);

function showSlide() {{
  showingPanel = false;
  stage.innerHTML = `<img class="slide" src="${{slides[index]}}">`;
  label.textContent = `Slide ${{index + 1}}/${{slides.length}} • 10 segundos`;
  index++;
  if (index >= slides.length) {{ index = 0; showingPanel = true; }}
  setTimeout(() => {{ showingPanel ? showPanel() : showSlide(); }}, 10000);
}}

function showPanel() {{
  stage.innerHTML = `<div id="panelWrap"><iframe id="panelFrame" src="${{panelUrl}}&cache=${{Date.now()}}"></iframe></div>`;
  label.textContent = 'Painel Apputivo • MODO TV • 30 segundos';
  scalePanel();
  setTimeout(showSlide, 30000);
}}

showSlide();
</script>
</body>
</html>
"""

components.html(html, height=1080, scrolling=False)
