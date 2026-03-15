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
m1, m2, m3 = st.columns(3
