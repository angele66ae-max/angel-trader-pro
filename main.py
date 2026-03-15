import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
from datetime import datetime
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE", initial_sidebar_state="collapsed")

# --- ESTILO Y FONDO (RUEDA DE MAHORA) ---
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)), url("{FONDO_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .card {{
        background: rgba(10, 15, 20, 0.85);
        border: 2px solid #00f2ff;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
    }}
    .metric-val {{
        font-size: 34px;
        color: #00f2ff;
        font-weight: bold;
        text-shadow: 0 0 10px #00f2ff;
    }}
    h1, h2, h3 {{ color: white !important; }}
</style>
""", unsafe_allow_html=True)

# --- CARTERA REAL (BITSO SYNC) ---
# Valores exactos de tu última captura
balance_mxn = 116.1
wallet = {
    "ETH": 0.0017524,
    "USD": 2.8,
    "CRONOS": 1.3972,
    "GOLEM": 2.3795,
    "BTC": 0.0000039
}

def get_live_price():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd", timeout=5)
        return float(r.json()['payload']['last'])
    except:
        return 71480.0

# --- LÓGICA DE DATOS ---
if "precios_log" not in st.session_state:
    st.session_state.precios_log = [get_live_price()]

current_p = get_live_price()
st.session_state.precios_log.append(current_p)
if len(st.session_state.precios_log) > 40: st.session_state.precios_log.pop(0)

# --- INTERFAZ MAHORASHARK ---
st.markdown("<h1 style='text-align:center;'>⛩️ MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)

# Dashboard Superior - FIX: Paréntesis cerrado en st.columns(3)
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="card">BALANCE TOTAL (USD)<div class="metric-val">${wallet["USD"]:.2f}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="card">GANANCIA LÍQUIDA<div class="metric-val" style="color:#ffd700;">+$0.3600</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="card">META SUV 10K<div class="metric-val" style="color:magenta;">0.0681%</div></div>', unsafe_allow_html=True)

st.write("")
col_chart, col_vault = st.columns([2, 1])

with col_chart:
    st.markdown("### Gráfica de Adaptación")
    # FIX: Definición de fig antes de llamar a plotly_chart
    fig = go.Figure(data=[go.Scatter(
        y=st.session_state.precios_log,
        mode='lines+markers',
        line=dict(color='#00f2ff', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 242, 255, 0.1)'
    )])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis_visible=False,
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', font=dict(color="white"))
    )
    st.plotly_chart(fig, use_container_width=True)

with col_vault:
    st.markdown('<div class="card" style="height:380px; text-align:left;">', unsafe_allow_html=True)
    st.subheader("Bóveda Mahora")
    st.write(f"**Pesos (MXN):** ${balance_mxn}")
    st.write(f"**Ether (ETH):** {wallet['ETH']}")
    st.write(f"**Dólares (USD):** ${wallet['USD']}")
    st.write(f"**Cronos:** {wallet['CRONOS']}")
    st.divider()
    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nAnalizando BTC...\nEstado: Prestige Activo.", language="bash")
    if st.button("🚀 FORZAR RE-ADAPTACIÓN", use_container_width=True):
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Auto-update
time.sleep(4)
st.rerun()
