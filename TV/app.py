
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os, time

st.set_page_config(layout="wide")

st.markdown("""
<style>
header, footer, #MainMenu {
    visibility:hidden;
}
.block-container {
    padding-top:0rem;
    padding-bottom:0rem;
    padding-left:0rem;
    padding-right:0rem;
    max-width:100%;
}
</style>
""", unsafe_allow_html=True)

slides_dir = "slides"

slides = sorted([
    os.path.join(slides_dir, x)
    for x in os.listdir(slides_dir)
    if x.endswith(".png")
])

if "inicio" not in st.session_state:
    st.session_state.inicio = time.time()

tempo = int(time.time() - st.session_state.inicio)

tempo_slide = 10
tempo_app = 30

total_slides = len(slides)

ciclo = (total_slides * tempo_slide) + tempo_app
pos = tempo % ciclo

if pos < total_slides * tempo_slide:

    idx = pos // tempo_slide

    st.image(slides[idx], use_container_width=True)

else:

    st.components.v1.html("""
    <script>
    window.location.href = "https://painel-apputivo-2ze4gkolje3kt8orpk4laa.streamlit.app/?modo=tv";
    </script>
    """, height=1)

st_autorefresh(interval=1000, key="refresh")
