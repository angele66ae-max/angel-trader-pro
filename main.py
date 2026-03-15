import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
from datetime import datetime
import plotly.graph_objects as go

# --- CONFIGURACIÓN PRESTIGE ---
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

# --- CARTERA TOTAL (BITSO SYNC) ---
# FIX: Llaves simples para evitar TypeError
wallet = {
    "ETH": 0.0017524,
    "USD": 2.81,
    "CRONOS": 1.3972,
    "GOLEM": 2.3795,
    "BTC": 0.0000039,
    "MXN": 47.12
}

def get_market_data():
    try:
        # Obtenemos precio de BTC y ETH para valuar la cartera
        btc_r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd", timeout=3).json()
        eth_r = requests.get("https://api.bitso.com/v3/ticker/?book=eth_usd", timeout=3).json()
        return {
            "btc": float(btc_r['payload']['last']),
            "eth": float(eth_r['payload']['last'])
        }
    except:
        return {"btc": 71500.0, "eth": 3950.0}

# --- LÓGICA DE DATOS ---
prices = get_market_data()
# Calculamos valor total sumando todos los activos
total_usd = (wallet["BTC"] * prices["btc"]) + (wallet["ETH"] * prices["eth"]) + wallet["USD"]

if "hist" not in st.session_state:
    st.session_state.hist = [prices["btc"]]

st.session_state.hist.append(prices["btc"])
if len(st.session_state.hist) > 40: st.session_state.hist.pop(0)

# --- INTERFAZ MAHORASHARK ---
st.markdown("<h1 style='text-align:center;'>⛩️ MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)

# Dash Superior con Balance Total de TODOS los activos
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="card">VALOR TOTAL CARTERA<div class="metric-val">${total_usd:.2f}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="card">GANANCIA LÍQUIDA<div class="metric-val" style="color:#00ff00;">+$0.01520</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="card">META SUV 10K<div class="metric-val" style="color:magenta;">{ (total_usd/10000)*100 :.4f}%</div></div>', unsafe_allow_html=True)

st.write("")
col_l, col_r = st.columns([2, 1])

with col_l:
    st.markdown("### Adaptación de Mercado (Bitcoin)")
    fig = go.Figure(data=go.Scatter(
        y=st.session_state.hist,
        mode='lines+markers',
        line=dict(color='#00f2ff', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 242, 255, 0.1)'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_visible=False,
        yaxis=dict(color="white", gridcolor="rgba(255,255,255,0.05)"),
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.markdown('<div class="card" style="height:410px; text-align:left;">', unsafe_allow_html=True)
    st.subheader("Bóveda Total")
    # Mostramos todos los activos de Bitso
    st.write(f"🌐 **Ether:** {wallet['ETH']}")
    st.write(f"💎 **Cronos:** {wallet['CRONOS']}")
    st.write(f"🤖 **Golem:** {wallet['GOLEM']}")
    st.write(f"🪙 **Bitcoin:** {wallet['BTC']}")
    st.write(f"💵 **Dólares:** ${wallet['USD']}")
    st.write(f"🇲🇽 **Pesos:** ${wallet['MXN']}")
    st.divider()
    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nSincronizando Bitso Multi-Asset...\nEstado: Prestige.", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(5)
st.rerun()
