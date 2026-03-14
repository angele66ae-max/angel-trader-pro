import streamlit as st
import pandas as pd
import numpy as np
import time
import json
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: PRESTIGE CENTER")

# URL DEL FONDO CÓSMICO (Rueda del Dharma)
URL_FONDO = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), 
                    url("{URL_FONDO}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #ffffff;
    }}
    .prestige-card {{
        background: rgba(10, 10, 10, 0.85);
        border: 2px solid rgba(0, 242, 255, 0.3);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(8px);
    }}
    .ai-logs {{
        background: rgba(0, 0, 0, 0.9);
        color: #00ff00;
        border: 1px solid #00ff00;
        padding: 10px;
        font-family: 'Courier New', monospace;
        height: 250px;
        overflow-y: auto;
    }}
</style>
""", unsafe_allow_html=True)

# --- DATOS Y LÓGICA CORREGIDA ---
precio_btc = 70711.0
balance_data = [{"currency": "usd", "available": "2.81"}]

# Corregido: Cierre de paréntesis y corchetes (Línea 90)
usd_real = next((i['available'] for i in balance_data if i['currency'] == 'usd'), "2.81")

# --- INTERFAZ MAHORASHARK ---
st.markdown("<h1 style='text-align:center; color:#00f2ff; font-family:sans-serif;'>⛩️ MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#e0e0e0;'>MAHORA ADAPTATION PROTOCOL v23.5</p>", unsafe_allow_html=True)

# Panel Superior: Métricas (Idéntico a tu captura de prestigio)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="prestige-card"><p style="color:cyan;">MERCADO DE BTC</p><h1>${precio_btc:,.0f}</h1></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="prestige-card"><p style="color:magenta;">SALDO DISPONIBLE</p><h1>${usd_real}</h1></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="prestige-card"><p style="color:green;">ESTADO DEL MOTOR</p><h1>ADAPTANDO</h1></div>', unsafe_allow_html=True)
with m4:
    # Meta SUV al 90.2%
    st.markdown('<div class="prestige-card"><p>OBJETIVO SUV</p><h1>90.2%</h1></div>', unsafe_allow_html=True)
    st.progress(0.902)

st.write("")

c_left, c_right = st.columns([2, 1])

with c_left:
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    st.subheader("Análisis de Adaptación")
    # Gráfica técnica (Corregido NameError: pd)
    df_chart = pd.DataFrame(np.random.randn(20, 1) + precio_btc, columns=['BTC Price'])
    st.area_chart(df_chart, color="#008080")
    st.markdown('</div>', unsafe_allow_html=True)

with c_right:
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    # Corregido: Cierre de paréntesis (Línea 97)
    st.markdown('<p style="font-size:18px;">🕵️ PENSAMIENTOS DE LA IA</p>', unsafe_allow_html=True)
    
    if st.button("🚀 INICIAR PROTOCOLO"):
        st.success("Adaptación Mahora en curso...")

    log_text = (
        f"[{time.strftime('%H:%M:%S')}] SISTEMA MAHORASHARK INICIADO\n"
        f"[INFO]: Analizando volatilidad...\n"
        f"[MERCADO]: Objetivo de venta fijado en 115."
    )
    st.markdown(f'<div class="ai-logs">{log_text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
