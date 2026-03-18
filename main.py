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

# --- 1. CONEXIÓN DE PODER (CREDENTIALS) ---
BITSO_KEY = "FZHAAOqOhy"
BITSO_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

# Reemplaza con tus llaves de Alpaca (Angel Capital Quant Fund)
ALP_KEY = "TU_ALPACA_KEY_REAL"
ALP_SECRET = "TU_ALPACA_SECRET_REAL"
alpaca = REST(ALP_KEY, ALP_SECRET, "https://paper-api.alpaca.markets")

st.set_page_config(layout="wide", page_title="Angel Capital Quant Fund")

# --- 2. MOTOR DE DATOS REALES ---
def get_bitso_balance():
    nonce = str(int(time.time() * 1000))
    signature = hmac.new(BITSO_SECRET.encode(), (nonce + "GET" + "/v3/balance/").encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {BITSO_KEY}:{nonce}:{signature}'}
    try:
        r = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        return {b['currency'].upper(): float(b['total']) for b in r['payload']['balances']}
    except:
        return {"MXN": 0.0}

def get_market_analysis(book):
    r = requests.get(f"https://api.bitso.com/v3/trades/?book={book}&limit=100").json()
    prices = [float(t['price']) for t in r['payload']]
    df = pd.DataFrame(prices, columns=['close'])
    df['rsi'] = ta.rsi(df['close'], length=14)
    df['ema_fast'] = ta.ema(df['close'], length=9)
    df['ema_slow'] = ta.ema(df['close'], length=21)
    return df.iloc[-1], prices[0]

# --- 3. LÓGICA DE EJECUCIÓN (COMPRA/VENTA) ---
def ejecutar_omni_trade(book, side, monto_mxn):
    path = "/v3/orders/"
    nonce = str(int(time.time() * 1000))
    payload = {"book": book, "side": side, "type": "market", "minor": f"{monto_mxn:.2f}"}
    json_payload = json.dumps(payload)
    sig = hmac.new(BITSO_SECRET.encode(), (nonce + "POST" + path + json_payload).encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {BITSO_KEY}:{nonce}:{sig}', 'Content-Type': 'application/json'}
    return requests.post(f"https://api.bitso.com{path}", headers=headers, data=json_payload).json()

# --- 4. INTERFAZ ANGEL CAPITAL ---
st.title("⛩️ Angel Capital Quant Fund: Mahorashark v17")

# Obtener Balances Reales
balances = get_bitso_balance()
mxn_real = balances.get('MXN', 0.0)

c1, c2, c3 = st.columns(3)
c1.metric("BALANCES MXN (BITSO)", f"${mxn_real:,.2f}")
# Aquí sumamos acciones si tienes cuenta conectada
c2.metric("META USD", "$10,000", delta=f"{(mxn_real/17.10):.2f} USD Actual")
c3.info("ESTADO: ESTRATEGIA QUANT ACTIVA")

st.write("---")

# --- 5. PANEL DE TRADING MULTI-ACTIVO ---
libros = ["btc_mxn", "sol_mxn", "eth_mxn"]
cols = st.columns(len(libros))

for i, book in enumerate(libros):
    data, precio = get_market_analysis(book)
    with cols[i]:
        st.subheader(book.upper())
        st.write(f"Precio: **${precio:,.2f}**")
        st.write(f"RSI: {data['rsi']:.2f}")
        
        # Estrategia: Cruce de EMA + RSI
        if data['ema_fast'] > data['ema_slow'] and data['rsi'] < 45:
            st.success("🎯 SEÑAL DE COMPRA")
            if mxn_real > 50:
                if st.button(f"Ejecutar {book}"):
                    res = ejecutar_omni_trade(book, "buy", mxn_real * 0.4)
                    st.json(res)
        else:
            st.warning("⚖️ ESPERANDO SEÑAL")

# --- 6. SECCIÓN DE BOLSA (STOCKS) ---
st.write("---")
st.subheader("📈 Mercado de Valores (NYSE/NASDAQ)")
stock_fav = st.selectbox("Analizar Acción", ["NVDA", "AAPL", "TSLA"])
stock_data = yf.Ticker(stock_fav).history(period="1d", interval="5m")
st.line_chart(stock_data['Close'])

if st.button(f"Comprar {stock_fav} en Alpaca"):
    # Esto compra $5 USD de la acción elegida
    try:
        order = alpaca.submit_order(symbol=stock_fav, notional=5, side='buy', type='market', time_in_force='day')
        st.success(f"Orden enviada a Wall Street: {order.id}")
    except Exception as e:
        st.error(f"Error en Alpaca: {e}")

time.sleep(20)
st.rerun()
