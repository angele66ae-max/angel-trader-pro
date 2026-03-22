import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="Angel Prestige Center", page_icon="⛩️")

# --- 2. ESTILO CSS (DISEÑO PRESTIGE) ---
st.markdown("""
    <style>
    .stApp { background: #0b141a; color: white; }
    .main-title { text-align: center; color: #e0fbfc; font-size: 28px; font-weight: bold; text-shadow: 0 0 10px #00f2ff; padding: 10px; border-bottom: 2px solid #00f2ff; }
    .kpi-container { background: rgba(16, 23, 30, 0.9); border: 2px solid #1f2937; border-radius: 10px; padding: 10px; text-align: center; }
    .console-box { background: #000; border: 2px solid #ff00ff; border-radius: 10px; padding: 15px; font-family: 'Courier New', monospace; color: #39FF14; height: 550px; overflow-y: auto; }
    .indicator-label { color: #00f2ff; font-weight: bold; font-size: 14px; text-align: center; background: rgba(0,242,255,0.1); padding: 5px; border-radius: 5px; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE DATOS (BITSO) ---
def fetch_bitso_data():
    try:
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn").json()['payload']
        df = pd.DataFrame(r)
        df['price'] = df['price'].astype(float)
        df['amount'] = df['amount'].astype(float)
        df['group'] = df.index // 4
        ohlc = df.groupby('group').agg({'price': ['first', 'max', 'min', 'last'], 'amount': 'sum'})
        ohlc.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        return ohlc, df['price'].iloc[0]
    except:
        # Valores de respaldo si falla el API
        return pd.DataFrame(), 1261324.0

ohlc_data, precio_actual = fetch_bitso_data()

# --- 4. RENDERIZADO DE INTERFAZ ---
st.markdown('<div class="main-title">⛩️ ANGEL\'S PRESTIGE OPERATIONAL CENTER</div>', unsafe_allow_html=True)
st.write("")

# FILA 1: KPIs SUPERIORES
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f'<div class="kpi-container"><small>BTC/MXN:</small><br><b style="color:#00f2ff; font-size:18px;">${precio_actual:,.0f} (+2.1%)</b></div>', unsafe_allow_html=True)
with k2:
    st.markdown('<div class="kpi-container"><small>MXN BALANCE:</small><br><b style="color:#ffffff; font-size:18px;">$115.59 (REAL)</b></div>', unsafe_allow_html=True)
with k3:
    st.markdown('<div class="kpi-container"><small>IA STATUS
