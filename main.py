import streamlit as st
import time, hashlib, hmac, json, requests
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE SEGURIDAD (Viene de tu secrets.toml) ---
API_KEY = st.secrets.get("BITSO_API_KEY", "")
API_SECRET = st.secrets.get("BITSO_API_SECRET", "")
BASE_URL = "https://api.bitso.com"

# --- MOTOR DE PRODUCCIÓN REAL ---
def trade_real_bitso(side, amount):
    """ESTA FUNCIÓN MANDA LA ORDEN A BITSO REAL"""
    path = "/v3/orders"
    nonce = str(int(time.time() * 1000))
    
    # Operamos con tus Dólares Digitales (USD) ya que tienes balance ahí
    payload = {
        "book": "btc_usd", 
        "side": side,
        "type": "market",
        "major": str(amount) if side == 'buy' else None,
        "minor": str(amount) if side == 'sell' else None
    }
    
    json_payload = json.dumps({k: v for k, v in payload.items() if v is not None})
    message = nonce + "POST" + path + json_payload
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    
    headers = {
        'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}',
        'Content-Type': 'application/json'
    }
    
    try:
        r = requests.post(BASE_URL + path, headers=headers, data=json_payload)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# --- OBTENER BALANCE REAL ---
def get_balance_real():
    path = "/v3/balance"
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + path
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    
    try:
        r = requests.get(BASE_URL + path, headers=headers)
        balances = r.json()['payload']['balances']
        # Buscamos tus USD y BTC
        usd = next(i['available'] for i in balances if i['currency'] == 'usd')
        btc = next(i['available'] for i in balances if i['currency'] == 'btc')
        return float(usd), float(btc)
    except:
        return 0.0, 0.0

# --- INTERFAZ SHARK REAL ---
usd_real, btc_real = get_balance_real()

st.title("🦈 SHARK AI: MODO PRODUCCIÓN REAL")

c1, c2 = st.columns(2)
with c1:
    st.metric("TU SALDO REAL (USD)", f"${usd_real:.2f}")
with c2:
    st.metric("TU SALDO REAL (BTC)", f"{btc_real:.8f}")

# --- LÓGICA DE ACTIVACIÓN ---
if st.button("🔴 ACTIVAR TRADING REAL"):
    st.session_state.modo_real = True
    st.warning("IA CAZANDO CON DINERO REAL EN BITSO")

if st.session_state.get("modo_real", False):
    # Aquí iría tu cálculo de RSI real
    # rsi_actual = conseguir_rsi_bitso()
    
    if rsi_actual < 30 and usd_real > 1:
        st.write("🟢 Ejecutando Compra Real...")
        res = trade_real_bitso("buy", 1) # Compra 1 USD de BTC
        st.json(res)
    elif rsi_actual > 70 and btc_real > 0.00001:
        st.write("🔴 Ejecutando Venta Real...")
        res = trade_real_bitso("sell", 0.00001)
        st.json(res)

time.sleep(10)
st.rerun()
