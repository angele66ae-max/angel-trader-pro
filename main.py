import streamlit as st
import yfinance as yf # <-- MOTOR DE ACCIONES
import pandas as pd
import pandas_ta as ta
import requests
import hmac
import hashlib
import time
import json

# --- 1. CONFIGURACIÓN DE CRIPTOS + STOCKS ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"
STOCKS_RADAR = ["NVDA", "TSLA", "AAPL"] # Acciones para el análisis de tendencia
LIBROS_BITSO = ["btc_mxn", "sol_mxn", "eth_mxn"]

st.set_page_config(layout="wide", page_title="MAHORA OMNI-MARKET")

# --- 2. MOTOR DE ACCIONES (WALL STREET) ---
def get_stock_sentiment():
    try:
        # Analizamos NVIDIA como termómetro del mercado tecnológico
        nvda = yf.Ticker("NVDA").history(period="1d", interval="5m")
        if nvda.empty: return "NEUTRAL", 0
        
        last_price = nvda['Close'].iloc[-1]
        open_price = nvda['Open'].iloc[0]
        change = ((last_price - open_price) / open_price) * 100
        
        sentiment = "BULLISH 🚀" if change > 0.5 else "BEARISH 📉" if change < -0.5 else "LATERAL ⚖️"
        return sentiment, change
    except:
        return "ERROR", 0

# --- 3. EJECUCIÓN REAL EN BITSO ---
def ejecutar_orden_bitso(book, side, monto):
    path = "/v3/orders/"
    nonce = str(int(time.time() * 1000))
    payload = {"book": book, "side": side, "type": "market", "minor": f"{monto:.2f}"}
    json_payload = json.dumps(payload)
    signature = hmac.new(API_SECRET.encode(), (nonce + "POST" + path + json_payload).encode(), hashlib.sha256).hexdigest()
    
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}', 'Content-Type': 'application/json'}
    r = requests.post(f"https://api.bitso.com{path}", headers=headers, data=json_payload)
    return r.json()

# --- 4. DASHBOARD OMNI ---
st.title("⛩️ MAHORASHARK: OMNI-MARKET ADAPTATION")

# Radar de Acciones (Lo que pediste)
sentimiento, variacion = get_stock_sentiment()

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("SENTIMIENTO WALL STREET (NVDA)", sentimiento, f"{variacion:.2f}%")
with c2:
    st.metric("CAPITAL DISPONIBLE", "$68.91 MXN") #
with c3:
    st.info("ESTRATEGIA: Sincronización Cripto-Acciones")

st.write("---")

# --- 5. LÓGICA DE DECISIÓN CRUZADA ---
st.subheader("🤖 Decisiones del Cerebro Mahora")

if sentimiento == "BULLISH 🚀":
    st.success("✅ Acciones subiendo: La IA buscará compras agresivas en SOL/BTC.")
    # Aquí el bot dispara compras en Bitso porque el mercado global es positivo
    for book in LIBROS_BITSO:
        # Lógica simplificada para ver acción:
        if variacion > 1.0: # Si NVIDIA sube más de 1%, compramos $20 MXN de SOL
            res = ejecutar_orden_bitso("sol_mxn", "buy", 20.00)
            st.code(f"ORDEN OMNI EJECUTADA: {res}")
            break
elif sentimiento == "BEARISH 📉":
    st.error("⚠️ Acciones cayendo: La IA se mantiene en MXN para proteger el capital.")
else:
    st.write(">> Esperando confirmación de tendencia en acciones para operar cripto.")

# Gráfica de la acción líder
st.write("### 📈 Monitor NVIDIA (NVDA) - Referencia Global")
data_nvda = yf.download("NVDA", period="1d", interval="15m")
st.line_chart(data_nvda['Close'])

time.sleep(30)
st.rerun()
