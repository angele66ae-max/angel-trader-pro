import streamlit as st
import pandas as pd
import pandas_ta as ta
import numpy as np
import requests
import hmac
import hashlib
import time
import json
import yfinance as yf
from alpaca_trade_api.rest import REST

# --- 1. CONFIGURACIÓN DE PODER ---
BITSO_KEY = "FZHAAOqOhy"
BITSO_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"
ALP_KEY = "AK2MF7RHHRDWLLX6R47FPZE32J"
ALP_SECRET = "4pDdU6jCS3zA7QB1aK4d68FTG6MobAgJnvh8vGTsMj47"
alpaca = REST(ALP_KEY, ALP_SECRET, "https://paper-api.alpaca.markets")

st.set_page_config(layout="wide", page_title="Angel Capital Quant Fund")

# --- 2. FUNCIONES DE EJECUCIÓN ---
def get_real_balance():
    nonce = str(int(time.time() * 1000))
    sig = hmac.new(BITSO_SECRET.encode(), (nonce + "GET" + "/v3/balance/").encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {BITSO_KEY}:{nonce}:{sig}'}
    try:
        r = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        return {b['currency'].upper(): float(b['total']) for b in r['payload']['balances']}
    except: return {"MXN": 0.0}

# --- 3. EL CEREBRO DE LA IA (RAZONAMIENTO) ---
def pensamiento_ia(rsi, precio, tendencia_wall_street, saldo_mxn):
    razonamiento = []
    accion_sugerida = "ESPERAR ⚖️"
    color = "#39FF14" # Neon Green

    if rsi < 35:
        razonamiento.append("• El RSI está en zona de sobreventa. El mercado está 'barato' técnicamente.")
    elif rsi > 65:
        razonamiento.append("• El RSI indica sobrecompra. Riesgo de corrección inminente.")
    
    if tendencia_wall_street > 0.5:
        razonamiento.append("• Wall Street (NVDA) tiene fuerza alcista. Hay confianza en el sector tech.")
    else:
        razonamiento.append("• Mercado tradicional lento. La liquidez podría estar estancada.")

    if saldo_mxn < 50:
        razonamiento.append("• Alerta: Saldo bajo ($" + str(saldo_mxn) + "). Operaciones limitadas.")

    # Decisión Final
    if rsi < 35 and tendencia_wall_street > 0:
        accion_sugerida = "COMPRA AGRESIVA 🚀"
        color = "#00FFFF" # Cyan
    elif rsi > 70 or (tendencia_wall_street < -1):
        accion_sugerida = "VENTA DE PÁNICO / PROTECCIÓN 🚨"
        color = "#FF00FF" # Magenta
    
    return razonamiento, accion_sugerida, color

# --- 4. INTERFAZ "PRESTIGE" ---
st.title("⛩️ MAHORASHARK: AI COGNITIVE TRADING")

balances = get_real_balance()
mxn_actual = balances.get('MXN', 0.0)

# Datos de Mercado
r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn&limit=100").json()
precios = [float(t['price']) for t in r['payload']]
rsi_val = ta.rsi(pd.Series(precios), length=14).iloc[-1]
nvda = yf.Ticker("NVDA").history(period="1d", interval="5m")
cambio_nvda = ((nvda['Close'].iloc[-1] - nvda['Open'].iloc[0]) / nvda['Open'].iloc[0]) * 100

# --- SECCIÓN: PENSAMIENTO DE LA IA ---
st.subheader("🧠 CÓRTEX CEREBRAL: ANÁLISIS EN TIEMPO REAL")
logs, decision, neon_color = pensamiento_ia(rsi_val, precios[0], cambio_nvda, mxn_actual)

with st.container():
    st.markdown(f"""
    <div style="background-color:#000; border:2px solid {neon_color}; padding:20px; border-radius:10px;">
        <h3 style="color:{neon_color
