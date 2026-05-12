
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from pathlib import Path
import time
import base64

st.set_page_config(
    page_title="Painel TV",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    margin: 0 !important;
    padding: 0 !important;
    background: black !important;
    overflow: hidden !important;
}
header, footer, #MainMenu {
    visibility: hidden !important;
    height: 0px !important;
}
.block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}
[data-testid="stVerticalBlock"] {
    gap: 0rem !important;
}
.slide-img {
    width: 100vw;
    height: 100vh;
    object-fit: contain;
    background: black;
    display: block;
}
.aviso {
    color: white;
    font-size: 32px;
    padding: 40px;
    font-family: Arial, sans-serif;
}
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent
SLIDES_DIR = BASE_DIR / "slides"

TEMPO_SLIDE = 10
TEMPO_APP = 30
APP_URL = "https://painel-apputivo-2ze4gkolje3kt8orpk4laa.streamlit.app/?modo=tv&tv=1"

# Cria a pasta slides automaticamente caso ela não exista.
SLIDES_DIR.mkdir(exist_ok=True)

slides = sorted([
    p for p in SLIDES_DIR.iterdir()
    if p.suffix.lower() in [".png", ".jpg", ".jpeg"]
])

if "inicio" not in st.session_state:
    st.session_state.inicio = time.time()

tempo_decorrido = int(time.time() - st.session_state.inicio)

if not slides:
    st.markdown(
        "<div class='aviso'>A pasta <b>slides</b> está vazia. Coloque as imagens dos slides em PNG ou JPG dentro dela.</div>",
        unsafe_allow_html=True
    )
else:
    total_slides = len(slides)
    ciclo_total = (total_slides * TEMPO_SLIDE) + TEMPO_APP
    posicao = tempo_decorrido % ciclo_total

    if posicao < total_slides * TEMPO_SLIDE:
        indice = posicao // TEMPO_SLIDE
        arquivo = slides[indice]

        with open(arquivo, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        st.markdown(
            f"<img class='slide-img' src='data:image/png;base64,{encoded}'>",
            unsafe_allow_html=True
        )

    else:
        # Não usa iframe, porque o Streamlit Cloud bloqueia e gera a tela cinza com X.
        st.markdown(
            f"""
            <script>
                window.top.location.href = "{APP_URL}";
            </script>
            <div class='aviso'>Abrindo painel em Modo TV...</div>
            """,
            unsafe_allow_html=True
        )

st_autorefresh(interval=1000, key="refresh_tv")
