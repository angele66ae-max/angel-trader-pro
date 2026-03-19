import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="MahoraShark: Prestige Center")

# --- ESTILO CSS CUSTOM ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: white; }
    .metric-card {
        background-color: #0b141a;
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 15px #00f2ff33;
    }
    .metric-title { color: #ffffff; font-size: 11px; font-weight: bold; text-transform: uppercase; }
    .metric-value { color: #00f2ff; font-size: 26px; font-weight: bold; text-shadow: 0 0 8px #00f2ff; }
    .coin-title { font-size: 14px; font-weight: bold; margin-top: 10px; }
    .coin-value { font-size: 24px; color: #ff00ff; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS ---
def obtener_bitso():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
        return float(r['payload']['last'])
    except: return 0.0

precio_btc = obtener_bitso()
saldo_mxn = 47.12
meta_10k = 10000.0
progreso_porcentaje = (saldo_mxn / meta_10k) * 100

# --- INTERFAZ ---
st.title("⛩️ MAHORASHARK: PRESTIGE CENTER")

# Fila Superior de Métricas
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">BTC/MXN BITSO</div><div class="metric-value">${precio_btc:,.0f}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric-card"><div class="metric-title">BALANCE REAL</div><div class="metric-value" style="color:#ff00ff">$2.81</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-card"><div class="metric-title">GANANCIA LÍQUIDA</div><div class="metric-value" style="color:#39FF14">+$0.01520</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><div class="metric-title">META 10K</div><div class="metric-value">{progreso_porcentaje:.4f}%</div></div>', unsafe_allow_html=True)

st.write("---")

# Cuerpo Principal
col_info, col_chart, col_ia = st.columns([1, 2, 1])

with col_info:
    st.subheader("Tu Cuenta")
    st.write("**Bitcoin (BTC)** \n ### 0.000039")
    st.write("**Ethereum (ETH)** \n ### 0.000000")
    st.write("**Pesos (MXN)** \n ### $47.12")
    st.write("**Dólares (USD)** \n ### $2.81")

with col_chart:
    st.subheader("Gráfica de Velas Japonesas (Profesional)")
    # Simulamos datos para la gráfica visual de velas
    chart_data = pd.DataFrame(np.random.randn(30, 2), columns=['Cian', 'Magenta'])
    st.line_chart(chart_data)

with col_ia:
    st.subheader("Cerebro Mahora")
    st.markdown(f'<div style="height:250px; border:2px solid #00f2ff; border-radius:10px; padding:15px; background:black; font-family:monospace; color:#00f2ff;">[SISTEMA]: ACTIVO<br>[IA]: Analizando...<br>[META]: $10,000.00</div>', unsafe_allow_html=True)
