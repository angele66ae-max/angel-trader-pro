import streamlit as st
import pandas as pd  # <--- ESTO CORRIGE EL NAMEERROR
import numpy as np   # <--- NECESARIO PARA GENERAR LA GRÁFICA
import time, json, requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="SHARK AI: PRESTIGE CENTER")

# URL DEL FONDO CÓSMICO
URL_FONDO = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), 
                    url("{URL_FONDO}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
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
        font-family: monospace;
        height: 250px;
        overflow-y: auto;
    }}
</style>
""", unsafe_allow_html=True)

# --- DATOS Y LÓGICA (CORREGIDO LÍNEA 90) ---
precio_btc = 70711.0
balance_simulado = [{"currency": "usd", "available": "2.81"}]

# Corregido: Se cierran todos los paréntesis del generador 'next'
usd_real = next((i['available'] for i in balance_simulado if i['currency'] == 'usd'), "2.81")

# --- INTERFAZ ---
st.markdown("<h1 style='text-align:center; color:#00f2ff; font-family:sans-serif;'>SHARK AI: PRESTIGE CENTER</h1>", unsafe_allow_html=True)

# Métrica Superior
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="prestige-card"><p style="color:cyan;">MERCADO DE BTC</p><h1>${precio_btc:,.0f}</h1></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="prestige-card"><p style="color:magenta;">SALDO DISPONIBLE</p><h1>${usd_real}</h1></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="prestige-card"><p style="color:green;">ESTADO</p><h1>ADAPTANDO</h1></div>', unsafe_allow_html=True)
with m4:
    # Meta SUV al 90.2%
    st.markdown('<div class="prestige-card"><p>OBJETIVO SUV</p><h1>90.2%</h1></div>', unsafe_allow_html=True)
    st.progress(0.902)

st.write("")

c_left, c_right = st.columns([2, 1])

with c_left:
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    st.subheader("Live Analysis - Multi-Mercado")
    # Gráfica corregida (Ya no dará NameError)
    df_chart = pd.DataFrame(np.random.randn(20, 1) + precio_btc, columns=['BTC'])
    st.area_chart(df_chart, color="#008080")
    st.markdown('</div>', unsafe_allow_html=True)

with c_right:
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    # Corregido: Paréntesis cerrado en st.markdown (Línea 97)
    st.markdown('<p style="font-size:18px;">🕵️ PENSAMIENTOS DE LA IA</p>', unsafe_allow_html=True)
    
    if st.button("🚀 DEPLOY AI"):
        st.info("Protocolo Mahora iniciado...")

    log_text = f"[{time.strftime('%H:%M:%S')}] OPERADOR: PAVO FREE FIRE\n[INFO]: Escaneando señales...\n[OBJETIVO]: Venta en 115."
    st.markdown(f'<div class="ai-logs">{log_text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
