import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="MahoraShark: Prestige Center", page_icon="🦈")

# --- ESTILO CSS CYBERPUNK ---
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
    .metric-value { color: #00f2ff; font-size: 24px; font-weight: bold; text-shadow: 0 0 8px #00f2ff; }
    .ia-log {
        background-color: #000;
        border: 1px solid #ff00ff;
        border-radius: 5px;
        padding: 10px;
        font-family: 'Courier New', monospace;
        color: #39FF14;
        font-size: 13px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE DATOS REALES (BITSO) ---
def obtener_datos_ohlc():
    try:
        # Obtenemos los últimos trades para simular velas (OHLC real requiere API Key o librería avanzada)
        # Usamos el ticker para el precio actual y trades para tendencia
        url = "https://api.bitso.com/v3/trades/?book=btc_mxn"
        r = requests.get(url).json()
        df = pd.DataFrame(r['payload'])
        df['price'] = df['price'].astype(float)
        return df
    except: return pd.DataFrame()

def calcular_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# --- PROCESAMIENTO ---
data = obtener_datos_ohlc()
precio_actual = data['price'].iloc[0] if not data.empty else 0.0
rsi_actual = calcular_rsi(data['price']).iloc[-1] if not data.empty else 50.0
sma_7 = data['price'].rolling(window=7).mean().iloc[-1] if not data.empty else precio_actual

# Lógica de Decisión
decision = "⚖️ ESPERAR"
if rsi_actual < 35: decision = "🟢 COMPRA ESTRATÉGICA"
elif rsi_actual > 65: decision = "🔴 VENTA / STOP LOSS"

# --- INTERFAZ ---
st.title("⛩️ MAHORASHARK: PRESTIGE CENTER")

# 📊 1. PANEL SUPERIOR
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">BTC/MXN REAL</div><div class="metric-value">${precio_actual:,.1f}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric-card"><div class="metric-title">BALANCE USD</div><div class="metric-value" style="color:#ff00ff
