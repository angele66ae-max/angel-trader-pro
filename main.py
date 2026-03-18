import streamlit as st
import pandas as pd
import pandas_ta as ta
import numpy as np  # <-- ERROR 1 CORREGIDO
import requests
import hmac
import hashlib
import time
import json
from datetime import datetime

# --- 1. CONFIGURACIÓN DE ACCESO SEGURO ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"
LIBROS = ["btc_mxn", "eth_mxn", "sol_mxn", "xrp_mxn"]

st.set_page_config(layout="wide", page_title="MAHORA PRO LIVE")

# --- 2. GESTIÓN DE MEMORIA (ERROR 2: EVITAR SPAM) ---
if "last_trade_time" not in st.session_state:
    st.session_state.last_trade_time = 0

# --- 3. FUNCIONES DE EJECUCIÓN REAL (POST) ---
def ejecutar_orden_real(book, side, amount_mxn):
    path = "/v3/orders/"
    nonce = str(int(time.time() * 1000))
    payload = {
        "book": book,
        "side": side,
        "type": "market",
        "minor": f"{amount_mxn:.2f}"
    }
    json_payload = json.dumps(payload)
    signature = hmac.new(API_SECRET.encode(), (nonce + "POST" + path + json_payload).encode(), hashlib.sha256).hexdigest()
    
    headers = {
        'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}',
        'Content-Type': 'application/json'
    }
    try:
        r = requests.post(f"https://api.bitso.com{path}", headers=headers, data=json_payload)
        st.session_state.last_trade_time = time.time() # Bloqueo de seguridad tras operar
        return r.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_rsi_real(book): # <-- ERROR 3: RSI REAL CORREGIDO
    try:
        r = requests.get(f"https://api.bitso.com/v3/trades/?book={book}&limit=50").json()
        trades = r['payload']
        prices = [float(t['price']) for t in trades]
        df = pd.DataFrame(prices, columns=['close'])
        rsi_series = ta.rsi(df['close'], length=14)
        return rsi_series.iloc[-1] if not rsi_series.empty else 50
    except:
        return 50

def get_balances():
    nonce = str(int(time.time() * 1000))
    signature = hmac.new(API_SECRET.encode(), (nonce + "GET" + "/v3/balance/").encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    r = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
    return {b['currency'].upper(): float(b['total']) for b in r['payload']['balances']}

# --- 4. LÓGICA DE TRADING ACTIVA ---
st.title("⛩️ MAHORASHARK: FULL AUTO V13")
balances = get_balances()
mxn_disponible = balances.get('MXN', 0)

# ERROR 4: CONTROL DE CAPITAL (Máximo 30% por moneda)
capital_por_trade = mxn_disponible * 0.30 

c1, c2, c3 = st.columns(3)
c1.metric("CAPITAL MXN", f"${mxn_disponible:,.2f}")
c2.metric("MODO", "TOTAL AUTÓNOMO")
tiempo_desde_ultimo = int(time.time() - st.session_state.last_trade_time)
c3.write(f"⏱️ Segundos desde último trade: {tiempo_desde_ultimo}s")

st.write("---")
logs = []

# --- 5. EL MOTOR DE DISPARO ---
cols = st.columns(len(LIBROS))

for i, book in enumerate(LIBROS):
    rsi_actual = get_rsi_real(book)
    ticker = requests.get(f"https://api.bitso.com/v3/ticker/?book={book}").json()['payload']
    precio = float(ticker['last'])
    moneda = book.split("_")[0].upper()
    
    with cols[i]:
        st.write(f"**{book.upper()}**")
        st.write(f"RSI: {rsi_actual:.2f}")
        
        # ¿PODEMOS OPERAR? (Seguridad: 60s entre trades y saldo > $50)
        puede_operar = (time.time() - st.session_state.last_trade_time) > 60

        if rsi_actual < 30 and mxn_disponible > 50 and puede_operar:
            res = ejecutar_orden_real(book, "buy", capital_por_trade)
            logs.append(f"🟢 COMPRA REAL {book}: {res}")
            
        elif rsi_actual > 70 and balances.get(moneda, 0) > 0.00001 and puede_operar:
            # Venta del activo si el RSI está alto
            res = ejecutar_orden_real(book, "sell", capital_por_trade)
            logs.append(f"🔴 VENTA REAL {book}: {res}")

# --- 6. INTERFAZ DE LOGS ---
st.subheader("📜 EJECUCIÓN EN TIEMPO REAL")
if logs:
    for l in logs: st.code(l)
else:
    st.write(">> Escaneando mercados con datos reales... Esperando señal óptima.")

time.sleep(15)
st.rerun()
