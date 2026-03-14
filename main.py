import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- CONFIGURACIÓN DE NÚCLEO ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: BITSO LIVE")

# --- RECUPERACIÓN DEL FONDO (Enlace corregido) ---
# Se utiliza el enlace directo para que Streamlit pueda renderizar la imagen de fondo
fondo_directo = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                    url("{fondo_directo}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .card {{
        background: rgba(10, 10, 15, 0.9);
        border: 2px solid #00f2ff;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
    }}
    .stMetric {{
        background: rgba(0, 0, 0, 0.3);
        padding: 10px;
        border-radius: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# --- MEMORIA DE SESIÓN (IA Y DATOS) ---
if "precios_hist" not in st.session_state:
    st.session_state.precios_hist = list(np.random.normal(70965, 10, size=50))
if "logs_ia" not in st.session_state:
    st.session_state.logs_ia = [f"[{datetime.now().strftime('%H:%M:%S')}] BITSO: Conexión establecida."]

# --- LÓGICA FINANCIERA ---
META = 10000.0
balance = 2.81
progreso = (balance / META)

st.markdown("<h1 style='text-align:center; color:#00f2ff; font-family:sans-serif;'>⛩️ MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)

# Dashboard Superior
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="card">ESTADO BITSO<br><h2 style="color:#00ff00;">GENERANDO</h2></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="card">BALANCE USD<br><h2 style="color:magenta;">${balance:.2f}</h2></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="card">OBJETIVO VENTA<br><h2>115</h2></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="card">META SUV<br><h2>{(progreso*100):.4f}%</h2></div>', unsafe_allow_html=True)
    st.progress(progreso if progreso <= 1.0 else 1.0)

st.write("")

# --- CUERPO TÉCNICO ---
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Análisis de Volatilidad (BTC/USD)")
