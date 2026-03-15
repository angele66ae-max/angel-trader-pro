import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
from datetime import datetime
import plotly.graph_objects as go

# --- NÚCLEO PRESTIGE ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE", initial_sidebar_state="collapsed")

# --- FONDO DE LA RUEDA ---
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("{FONDO_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .card {{
        background: rgba(10, 20, 30, 0.85);
        border: 2px solid #00f2ff;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
    }}
    .metric-val {{
        font-size: 38px;
        color: #00f2ff;
        font-weight: bold;
        text-shadow: 0 0 10px #00f2ff;
    }}
    h1, h3, p {{ color: white !important; font-family: 'Segoe UI', sans-serif; }}
</style>
""", unsafe_allow_html=True)

# --- CARTERA SYNC (BITSO) ---
# Datos exactos de tu wallet
mxn_total = 116.1
usd_balance = 2.81
wallet = {
    "ETH": 0.0017524,
    "CRONOS": 1.3972,
    "GOLEM": 2.3795,
    "BTC": 0.0000039
}

def get_price():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd", timeout=3)
        return float(r.json()['payload']['last'])
    except:
        return 71450.0

# --- LÓGICA DE DATOS ---
if "precios" not in st.session_state:
    st.session_state.precios = [get_price()]

current_p = get_price()
st.session_state.precios.append(current_p)
if len(st.session_state.precios) > 30: st.session_state.precios.pop(0)

# --- INTERFAZ ---
st.markdown("<h1 style='text-align:center;'>⛩️ MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)

# Dash Superior
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="card">BALANCE USD<div class="metric-val">${usd_balance}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="card">BALANCE MXN<div class="metric-val" style="color:#00ff00;">${mxn_total}</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="card">META SUV 10K<div class="metric-val" style="color:magenta;">0.0681%</div></div>', unsafe_allow_html=True)

st.write("")
c_left, c_right = st.columns([2, 1])

with c_left:
    st.markdown("### Gráfica de Adaptación (BTC/USD)")
    # Simplificación de la gráfica para evitar ValueError
    fig = go.Figure(data=go.Scatter(
        y=st.session_state.precios,
        mode='lines+markers',
        line=dict(color='#00f2ff', width=3),
        fill='tozeroy'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_visible=False,
        yaxis=dict(color="white", gridcolor="rgba(255,255,255,0.1)"),
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

with c_right:
    st.markdown('<div class="card" style="height:400px; text-align:left;">', unsafe_allow_html=True)
    st.subheader("Bóveda Mahora")
    st.write(f"🔹 **Ether:** {wallet['ETH']}")
    st.write(f"🔹 **Cronos:** {wallet['CRONOS']}")
    st.write(f"🔹 **Golem:** {wallet['GOLEM']}")
    st.write(f"🔹 **Bitcoin:** {wallet['BTC']}")
    st.divider()
    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nAnalizando Multidivisa...\nEstado: Prestige Estable.", language="bash")
    if st.button("🚀 FORZAR ADAPTACIÓN", use_container_width=True):
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Refresco
time.sleep(5)
st.rerun()
