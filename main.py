import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
from datetime import datetime
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE NÚCLEO ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

# --- FONDO GALÁCTICO MAHORA ---
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{FONDO_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .card {{
        background: rgba(10, 10, 15, 0.85);
        border: 1px solid #00f2ff;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
    }}
    .metric-val {{
        font-size: 32px;
        color: #00f2ff;
        font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# --- DATOS REALES (BITSO WALLET) ---
# Valores extraídos de tu captura de Bitso
wallet = {
    "ETH": 0.0017524,
    "USD": 2.81,
    "CRONOS": 1.3972,
    "GOLEM": 2.3795,
    "BTC": 0.0000039
}

def get_btc_price():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd", timeout=5)
        return float(r.json()['payload']['last'])
    except:
        return 71450.0

# --- LÓGICA DE INTERFAZ ---
if "precios_hist" not in st.session_state:
    st.session_state.precios_hist = [get_btc_price()]

price = get_btc_price()
st.session_state.precios_hist.append(price)
if len(st.session_state.precios_hist) > 50: st.session_state.precios_hist.pop(0)

st.markdown("<h1 style='text-align:center; color:#00f2ff;'>⛩️ MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)

# Dashboard Superior
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="card">BALANCE TOTAL (USD)<div class="metric-val">${wallet["USD"] + 3.61:.2f}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="card">GANANCIA REAL<div class="metric-val" style="color:#ffd700;">+$0.36000</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="card">META SUV 10K<div class="metric-val" style="color:magenta;">0.0681%</div></div>', unsafe_allow_html=True)

st.write("")
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown('<h3 style="color:white;">Gráfica de Adaptación (BTC/USD)</h3>', unsafe_allow_html=True)
    fig
