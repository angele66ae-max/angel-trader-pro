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

# --- 1. CONEXIÓN DE PODER (Sincronizado con tus capturas) ---
BITSO_KEY = "FZHAAOqOhy"
BITSO_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

# Credenciales de tu imagen b2c6c1
ALP_KEY = "AK2MF7RHHRDWLLX6R47FPZE32J"
ALP_SECRET = "4pDdU6jCS3zA7QB1aK4d68FTG6MobAgJnvh8vGTsMj47"
# Cambiamos a la URL de LIVE para dinero real (o mantén paper para pruebas finales)
BASE_URL = "https://paper-api.alpaca.markets" 
alpaca = REST(ALP_KEY, ALP_SECRET, BASE_URL)

st.set_page_config(layout="wide", page_title="Angel Capital Quant Fund")

# --- 2. MOTOR DE EJECUCIÓN REAL ---
def enviar_orden_bitso(book, side, monto_mxn):
    path = "/v3/orders/"
    nonce = str(int(time.time() * 1000))
    payload = {"book": book, "side": side, "type": "market", "minor": f"{monto_mxn:.2f}"}
    json_payload = json.dumps(payload)
    sig = hmac.new(BITSO_SECRET.encode(), (nonce + "POST" + path + json_payload).encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {BITSO_KEY}:{nonce}:{sig}', 'Content-Type': 'application/json'}
    try:
        r = requests.post(f"https://api.bitso.com{path}", headers=headers, data=json_payload)
        return r.json()
    except Exception as e: return {"success": False, "error": str(e)}

def get_real_balance():
    nonce = str(int(time.time() * 1000))
    sig = hmac.new(BITSO_SECRET.encode(), (nonce + "GET" + "/v3/balance/").encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {BITSO_KEY}:{nonce}:{sig}'}
    r = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
    return {b['currency'].upper(): float(b['total']) for b in r['payload']['balances']}

# --- 3. DASHBOARD "PRESTIGE" ---
st.title("⛩️ MAHORASHARK: REAL MONEY MODE")

balances = get_real_balance()
mxn_actual = balances.get('MXN', 0.0)

c1, c2, c3 = st.columns(3)
c1.metric("SALDO REAL BITSO", f"${mxn_actual:,.2f} MXN")
c2.metric("SISTEMA", "ADAPTACIÓN ACTIVA", delta="LIVE")
c3.metric("META", "$10,000 USD", delta=f"{(mxn_actual/17.10):.2f} USD")

# --- 4. CEREBRO DE TRADING (Venta de Pánico + Compra) ---
st.write("---")
libro = "btc_mxn"
# Obtenemos datos para el análisis
r = requests.get(f"https://api.bitso.com/v3/trades/?book={libro}&limit=100").json()
prices = [float(t['price']) for t in r['payload']]
df = pd.DataFrame(prices, columns=['close'])
df['rsi'] = ta.rsi(df['close'], length=14)
rsi_now = df['rsi'].iloc[-1]
precio_now = prices[0]

# --- LÓGICA DE PROTECCIÓN (STOP LOSS) ---
# Si el precio cae 5% de tu última compra, el bot vende todo.
if "precio_compra" not in st.session_state:
    st.session_state.precio_compra = precio_now

stop_loss = st.session_state.precio_compra * 0.95 

st.subheader(f"🛡️ Protección de Capital ({libro.upper()})")
col_p1, col_p2 = st.columns(2)
col_p1.write(f"Precio Actual: **${precio_now:,.2f}**")
col_p2.write(f"Nivel de Venta de Pánico: **${stop_loss:,.2f}**")

# --- EJECUCIÓN AUTOMÁTICA ---
if precio_now <= stop_loss:
    st.error("🚨 ¡VENTA DE PÁNICO ACTIVADA! Protegiendo capital...")
    # Lógica para vender lo que tengas de BTC
    btc_disponible = balances.get('BTC', 0.0)
    if btc_disponible > 0.00001:
        res = enviar_orden_bitso(libro, "sell", btc_disponible * precio_now)
        st.json(res)

elif rsi_now < 30 and mxn_actual > 50:
    st.success("🟢 SEÑAL DE COMPRA: El RSI está bajo, oportunidad detectada.")
    if st.button("Ejecutar Compra Real"):
        res = enviar_orden_bitso(libro, "buy", mxn_actual * 0.5) # Usa el 50%
        st.session_state.precio_compra = precio_now
        st.json(res)

# --- 5. PUENTE A LA BOLSA (ALPACA) ---
st.write("---")
st.subheader("📈 Wall Street Bridge (NVIDIA)")
nvda = yf.Ticker("NVDA").history(period="1d", interval="1m")
st.line_chart(nvda['Close'])

if st.button("Comprar Fracción de Acción (Real)"):
    try:
        # Esto compra $5 USD de NVIDIA usando tus llaves de Alpaca
        res_alpaca = alpaca.submit_order(symbol="NVDA", notional=5, side='buy', type='market', time_in_force='day')
        st.success(f"Orden de Bolsa enviada: {res_alpaca.id}")
    except Exception as e:
        st.error(f"Error en Alpaca: {e}")

time.sleep(15)
st.rerun()
