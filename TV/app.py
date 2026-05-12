import base64
import os
import time
from pathlib import Path

import streamlit as st
from PIL import Image
from streamlit_autorefresh import st_autorefresh

# =====================================================
# CONFIGURAÇÕES
# =====================================================
TEMPO_SLIDE = 10          # segundos em cada slide
TEMPO_PAINEL = 30         # segundos no painel
PASTA_SLIDES = Path("slides")
PASTA_CACHE = Path("cache")
PASTA_CACHE.mkdir(exist_ok=True)

PAINEL_URL = "https://painel-apputivo-2ze4gkolje3kt8orpk4laa.streamlit.app/?tv=1&modo=tv&modo_tv=1"
SCREENSHOT_PAINEL = PASTA_CACHE / "painel_tv.png"

# =====================================================
# PÁGINA / CSS
# =====================================================
st.set_page_config(page_title="Painel TV", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {
    margin: 0 !important;
    padding: 0 !important;
    background: #000 !important;
    overflow: hidden !important;
}
[data-testid="stHeader"], header, footer, #MainMenu {display:none !important; visibility:hidden !important; height:0 !important;}
.block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100vw !important;
    width: 100vw !important;
}
img {
    width: 100vw !important;
    height: 100vh !important;
    object-fit: contain !important;
    background: #000 !important;
    display: block !important;
}
.painel-aviso {
    color: white;
    font-family: Arial, sans-serif;
    padding: 32px;
    font-size: 26px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNÇÕES
# =====================================================
def listar_slides():
    if not PASTA_SLIDES.exists():
        return []
    return sorted([
        p for p in PASTA_SLIDES.iterdir()
        if p.suffix.lower() in [".png", ".jpg", ".jpeg"]
    ])


def mostrar_imagem_tela_cheia(caminho):
    with open(caminho, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    st.markdown(
        f'<img src="data:image/png;base64,{b64}" />',
        unsafe_allow_html=True,
    )


def capturar_painel():
    """Captura o painel como imagem. Isso evita erro de iframe/redirect do Streamlit Cloud."""
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
            page.goto(PAINEL_URL, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(8000)

            # Tenta forçar modo TV caso exista controle na página
            try:
                page.evaluate("""
                    () => {
                        const labels = Array.from(document.querySelectorAll('label, span, div, p'));
                        const tv = labels.find(el => (el.innerText || '').toLowerCase().includes('modo tv'));
                        if (tv) tv.click();
                        document.body.style.zoom = '1';
                    }
                """)
                page.wait_for_timeout(2000)
            except Exception:
                pass

            page.screenshot(path=str(SCREENSHOT_PAINEL), full_page=False)
            browser.close()
            return True, ""
    except Exception as e:
        return False, str(e)


# =====================================================
# CICLO DE EXIBIÇÃO
# =====================================================
slides = listar_slides()
qtd_slides = len(slides)

if qtd_slides == 0:
    st.markdown('<div class="painel-aviso">Nenhum slide encontrado na pasta slides.</div>', unsafe_allow_html=True)
    st.stop()

if "inicio" not in st.session_state:
    st.session_state.inicio = time.time()

segundos = int(time.time() - st.session_state.inicio)
tempo_slides_total = qtd_slides * TEMPO_SLIDE
tempo_ciclo_total = tempo_slides_total + TEMPO_PAINEL
posicao = segundos % tempo_ciclo_total

# Atualiza a tela a cada 1 segundo
st_autorefresh(interval=1000, key="refresh_tv")

# Slides: 10 segundos cada
if posicao < tempo_slides_total:
    indice = posicao // TEMPO_SLIDE
    mostrar_imagem_tela_cheia(slides[indice])

# Painel: 30 segundos como captura de tela, sem iframe
else:
    precisa_atualizar = True
    if SCREENSHOT_PAINEL.exists():
        idade = time.time() - SCREENSHOT_PAINEL.stat().st_mtime
        precisa_atualizar = idade > 25

    if precisa_atualizar:
        with st.spinner("Carregando painel em Modo TV..."):
            ok, erro = capturar_painel()
        if not ok and not SCREENSHOT_PAINEL.exists():
            st.markdown(
                f'<div class="painel-aviso">Não foi possível capturar o painel.<br><br>'
                f'Execute uma vez:<br><br>'
                f'python -m playwright install chromium<br><br>'
                f'Detalhe: {erro}</div>',
                unsafe_allow_html=True,
            )
            st.stop()

    mostrar_imagem_tela_cheia(SCREENSHOT_PAINEL)
