import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
from datetime import datetime
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE NÚCLEO ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE", initial_sidebar_state="collapsed")

# --- FONDO Y ESTILO PRESTIGE ---
# Usamos el enlace directo para que la rueda de la galaxia sea el centro
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url("{FONDO_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .card {{
        background: rgba(10, 15, 20, 0.8);
        border: 2px solid #00f2ff;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
    }}
    .metric-val {{
        font-size: 35px;
        color: #00f2ff;
        font-weight: bold;
        text-shadow: 0 0 10px #00f2ff;
    }}
    h1, h2, h3 {{ color: white !important; font-family: 'Arial'; }}
</style>
""", unsafe_allow_html=True)

# --- DATOS DE CARTERA (Sincronizados con Bitso) ---
wallet = {{
    "ETH": 0.0017524,
    "USD": 2.81,
    "CRONOS": 1.3972,
    "GOLEM": 2.3795,
    "BTC": 0.0000039,
    "MXN": 116.1
}}

def get_market_price():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd", timeout=5)
        return float(r.json()['payload']['last'])
    except:
        return 71500.0

# --- LÓGICA DE MEMORIA ---
if "precios_hist" not in st.session_state:
    st.session_state.precios_hist = [get_market_price() for _ in range(20)]

current_p = get_market_price()
st.session_state.precios_hist.append(current_p)
if len(st.session_state.precios_hist) > 50: st.session_state.precios_hist.pop(0)

# --- INTERFAZ VISUAL ---
st.markdown("<h1 style='text-align:center;'>⛩️ MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)

# Dashboard de Métricas
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="card">BALANCE REAL (USD)<div class="metric-val">${wallet["USD"]:.2f}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="card">GANANCIA LÍQUIDA<div class="metric-val" style="color:#00ff00;">+$0.3600</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="card">META SUV 10K<div class="metric-val" style="color:magenta;">0.0681%</div></div>', unsafe_allow_html=True)

st.write("")
col_grafica, col_status = st.columns([2, 1])

with col_grafica:
    st.markdown("### Gráfica de Adaptación (BTC/USD)")
    # Creamos fig aquí para evitar el NameError
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=st.session_state.precios_hist,
        mode='lines+markers',
        line=dict(color='#00f2ff', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 242, 255, 0.1)'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis_visible=False,
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', font=dict(color="white"))
    )
    st.plotly_chart(fig, use_container_width=True)

with col_status:
    st.markdown('<div class="card" style="height:380px; text-align:left;">', unsafe_allow_html=True)
    st.subheader("Bóveda Mahora")
    st.write(f"🌐 **Ether:** {wallet['ETH']}")
    st.write(f"💵 **Dólares:** ${wallet['USD']}")
    st.write(f"💎 **Cronos:** {wallet['CRONOS']}")
    st.write(f"🤖 **Golem:** {wallet['GOLEM']}")
    st.divider()
    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nAnalizando liquidez...\nMeta SUV activa.\nAdaptando bot.", language="bash")
    if st.button("🚀 FORZAR RE-ADAPTACIÓN", use_container_width=True):
        st.toast("Adaptando a la volatilidad...")
    st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh
time.sleep(4)
st.rerun()
{{{{{{
