import streamlit as st
import pandas as pd
import numpy as np
import time

# --- CONFIGURACIÓN TÉCNICA ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: PRESTIGE")

# URL DIRECTA (Si esta falla, el código tiene un color de respaldo sólido)
URL_FONDO = "https://w0.peakpx.com/wallpaper/590/691/HD-wallpaper-mahaga-wheel-jujutsu-kaisen.jpg"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                    url("{URL_FONDO}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .prestige-card {{
        background: rgba(10, 10, 15, 0.9);
        border: 1px solid #00f2ff;
        border-radius: 10px;
        padding: 20px;
        color: white;
    }}
    .log-box {{
        background: black;
        color: #00ff00;
        padding: 15px;
        font-family: monospace;
        border: 1px solid #00ff00;
        height: 300px;
    }}
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE DATOS (Basada en tus capturas) ---
btc_price = 70965.50 #
balance = 2.81       #

# --- INTERFAZ ---
st.markdown("<h1 style='text-align:center; color:#00f2ff;'>⛩️ MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="prestige-card">PRECIO BTC<br><h2>${btc_price:,.2f}</h2></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="prestige-card">BALANCE REAL<br><h2>${balance:.2f}</h2></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="prestige-card">MOTOR IA<br><h2 style="color:#00ff00;">OPTIMIZADO</h2></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="prestige-card">META SUV<br><h2>90.2%</h2></div>', unsafe_allow_html=True)
    st.progress(0.902) #

st.write("")

c1, c2 = st.columns([2, 1])
with c1:
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    st.subheader("Gráfica de Rendimiento en Vivo")
    chart_data = pd.DataFrame(np.random.randn(50, 1).cumsum() + btc_price, columns=['Price'])
    st.line_chart(chart_data, color="#00f2ff")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    st.subheader("Pensamientos de la IA")
    if st.button("🚀 DEPLOY AI"):
        st.toast("Adaptación Mahora Iniciada")
    
    log_msg = f"[{time.strftime('%H:%M:%S')}] OPERADOR: MAHORASHARK\n[MERCADO]: Objetivo fijado en 115.\n[STATUS]: Produciendo dinero real."
    st.code(log_msg, language="bash")
    st.markdown('</div>', unsafe_allow_html=True)
