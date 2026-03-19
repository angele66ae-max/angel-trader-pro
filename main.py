import streamlit as st
import requests
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="MahoraShark Prestige")

# --- ESTILO CSS CUSTOM ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: white; }
    .metric-card {
        background-color: #0b141a;
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 10px #00f2ff55;
    }
    .metric-title { color: #ffffff; font-size: 12px; font-weight: bold; }
    .metric-value { color: #00f2ff; font-size: 24px; font-weight: bold; text-shadow: 0 0 5px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN CORREGIDA ---
def obtener_bitso():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
        return float(r['payload']['last'])
    except:
        return 0.0

# Llamada correcta a la función
precio_btc = obtener_bitso()

# --- INTERFAZ ---
st.title("⛩️ MAHORASHARK: PRESTIGE CENTER")

# Fila Superior
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">BTC/MXN BITSO</div><div class="metric-value">${precio_btc:,.1f}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric-card"><div class="metric-title">BALANCE REAL</div><div class="metric-value" style="color:#ff00ff">$2.81</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-card"><div class="metric-title">GANANCIA LÍQUIDA</div><div class="metric-value" style="color:#39FF14">+$0.01520</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="metric-card"><div class="metric-title">META 10K</div><div class="metric-value">0.0281%</div></div>', unsafe_allow_html=True)

st.write("") 

# Cuerpo
col_info, col_chart, col_ia = st.columns([1, 2, 1])

with col_info:
    st.subheader("Tu Cuenta")
    st.write("**Bitcoin (BTC)** \n ### 0.000039")
    st.write("**Pesos (MXN)** \n ### $47.12")

with col_chart:
    st.subheader("Gráfica de Velas (Simulada)")
    chart_data = pd.DataFrame(np.random.randn(30, 1), columns=['Precio'])
    st.line_chart(chart_data, color="#ff00ff")

with col_ia:
    st.subheader("Cerebro Mahora")
    st.markdown('<div style="height:200px; border:2px solid #00f2ff; border-radius:10px; padding:10px; background:black; font-family:monospace; color:#00f2ff;">[SISTEMA]: ONLINE<br>[IA]: Analizando...<br>[META]: $115.00</div>', unsafe_allow_html=True)
