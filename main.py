import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import time

# Intentamos cargar acciones sin que se rompa el sistema
try:
    import yfinance as yf
    ACCIONES_LISTAS = True
except ImportError:
    ACCIONES_LISTAS = False

st.set_page_config(layout="wide", page_title="MAHORASHARK MULTI-ASSET")

# --- DATOS REALES ---
MI_BTC = 0.00003542
META_USD = 115.00

st.markdown("<h1 style='color:#00f2ff; text-align:center;'>⛩️ MAHORASHARK: MULTI-ASSET V2</h1>", unsafe_allow_html=True)

if not ACCIONES_LISTAS:
    st.warning("⚠️ Módulo de Acciones no instalado. Ve a tu GitHub y añade 'yfinance' a requirements.txt")

# --- MONITOR DE MERCADO ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("₿ Cripto Bóveda")
    # Precio actual de Bitso
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
        p_btc = float(r['payload']['last'])
        valor_tu_btc = MI_BTC * p_btc
        st.metric("Tu Bitcoin (USD)", f"${valor_tu_btc:.2f}", delta=f"{((valor_tu_btc/META_USD)*100):.2f}% de la meta")
    except:
        st.error("Error conectando a Bitso")

with col2:
    st.subheader("📈 Monitor de Acciones")
    if ACCIONES_LISTAS:
        accion_buscada = st.text_input("Símbolo de Acción (ej: TSLA, AAPL, NVDA):", "TSLA")
        stock = yf.Ticker(accion_buscada)
        precio_accion = stock.history(period="1d")['Close'].iloc[-1]
        st.metric(f"Precio {accion_buscada}", f"${precio_accion:.2f} USD")
    else:
        st.info("Instale yfinance para ver precios de la bolsa aquí.")

st.write("---")
st.code(f"[{datetime.now().strftime('%H:%M:%S')}] Status: SYNCED | Mode: PRESTIGE", language="bash")

time.sleep(30)
st.rerun()
