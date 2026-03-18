import streamlit as st
import pandas as pd
import yfinance as yf
from alpaca_trade_api.rest import REST # pip install alpaca-trade-api
import requests
import hmac
import hashlib
import time
import json

# --- 1. CONEXIÓN BI-LATERAL ---
# Cripto (Bitso)
BITSO_KEY = "FZHAAOqOhy"
BITSO_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

# Bolsa (Alpaca) - Necesitas crear tu cuenta en alpaca.markets
ALP_KEY = "TU_ALPACA_KEY"
ALP_SECRET = "TU_ALPACA_SECRET"
alpaca = REST(ALP_KEY, ALP_SECRET, "https://paper-api.alpaca.markets")

st.set_page_config(layout="wide", page_title="MAHORA OMNI-EXCHANGE")

# --- 2. FUNCIONES DE INTERCAMBIO ---
def vender_cripto_comprar_accion(book, stock_symbol, monto_mxn):
    # Paso A: Vender en Bitso
    # (Aquí iría la función POST /v3/orders/ que ya tenemos)
    st.warning(f"🔄 Iniciando intercambio: Venta de {book} -> Compra de {stock_symbol}")
    
    # Paso B: Ejecutar compra en Wall Street
    # Calculamos cuántas acciones comprar con ese monto (aprox)
    try:
        alpaca.submit_order(
            symbol=stock_symbol,
            notional=monto_mxn / 17.10, # Convertimos MXN a USD para Alpaca
            side='buy',
            type='market',
            time_in_force='day'
        )
        return "✅ Intercambio Omni-Market Completado"
    except Exception as e:
        return f"❌ Error en el puente: {e}"

# --- 3. DASHBOARD DE CONTROL TOTAL ---
st.title("⛩️ MAHORASHARK: OMNI-TRADING BRIDGE")

# Monitoreo simultáneo
col_crypto, col_stocks = st.columns(2)

with col_crypto:
    st.subheader("₿ Mercado Cripto (Bitso)")
    btc_data = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()['payload']
    btc_price = float(btc_data['last'])
    st.metric("BTC/MXN", f"${btc_price:,.2f}")

with col_stocks:
    st.subheader("📈 Wall Street (NVDA)")
    nvda_data = yf.Ticker("NVDA").history(period="1d", interval="1m")
    nvda_price = nvda_data['Close'].iloc[-1]
    st.metric("NVIDIA USD", f"${nvda_price:.2f}")

st.write("---")

# --- 4. LÓGICA DE INTERCAMBIO (REBALANCEO) ---
st.subheader("🧠 Estrategia de Rotación de Capital")

# EJEMPLO: Si BTC sube mucho y NVDA está en oferta (RSI bajo), rotamos capital.
if btc_price > 1200000: # Precio de ejemplo para toma de ganancias
    st.success("🎯 BTC en zona de toma de ganancias. Sugerencia: Rotar a Acciones Tech.")
    
    if st.button("🚀 EJECUTAR ROTACIÓN: BTC -> NVDA"):
        res = vender_cripto_comprar_accion("btc_mxn", "NVDA", 500) # Rotar $500 MXN
        st.write(res)

else:
    st.info("⚖️ Manteniendo posiciones actuales. Esperando desequilibrio de mercado.")

# --- 5. VISUALIZACIÓN DE PROGRESO 10K ---
# Sumamos el valor de ambos mundos
total_usd = (btc_price / 17.10) + nvda_price # Simplificado
progreso = (total_usd / 10000) * 100
st.write(f"### Meta $10,000 USD: {progreso:.4f}%")
st.progress(min(progreso/100, 1.0))

time.sleep(30)
st.rerun()
