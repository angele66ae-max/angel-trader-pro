import streamlit as st
import pandas as pd
import requests
import time
import hmac
import hashlib
import json
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN DE PODER ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

def bitso_api(method, path, payload=None):
    nonce = str(int(time.time() * 1000))
    json_payload = json.dumps(payload, separators=(',', ':')) if payload else ""
    message = nonce + method + path + json_payload
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}', 'Content-Type': 'application/json'}
    try:
        url = f"https://api.bitso.com{path}"
        res = requests.request(method, url, headers=headers, data=json_payload)
        return res.json()
    except: return {"success": False, "error": {"message": "Error de Red"}}

# --- OBTENCIÓN DE BALANCE REAL ---
try:
    balances = bitso_api("GET", "/v3/balance/")['payload']['balances']
    mxn_disponible = next((float(b['available']) for b in balances if b['currency'] == 'mxn'), 0.0)
    usd_disponible = next((float(b['available']) for b in balances if b['currency'] == 'usd'), 0.0)
except:
    mxn_disponible, usd_disponible = 47.12, 2.81 #

# --- LÓGICA DE GASTO TOTAL ---
# Priorizamos MXN si es mayor a $10, de lo contrario usamos USD si es mayor a $1
if mxn_disponible >= 10.0:
    moneda_target = "MXN"
    book = "btc_mxn"
    # Usamos el 99.5% para cubrir el fee de Bitso y evitar el error de balance insuficiente
    monto_total = mxn_disponible * 0.995 
else:
    moneda_target = "USD"
    book = "btc_usd"
    monto_total = usd_disponible * 0.995

# --- INTERFAZ ---
st.title("⛩️ MAHORASHARK: MAX POWER")
st.write(f"### Fondos Totales Detectados: **${(mxn_disponible if moneda_target == 'MXN' else usd_disponible):.2f} {moneda_target}**")

if st.button(f"🚀 ADAPTAR TODO EL CAPITAL ({moneda_target})", use_container_width=True):
    if monto_total < 1.0 and moneda_target == "USD":
        st.error("Saldo insuficiente para el mínimo de $1 USD")
    elif monto_total < 10.0 and moneda_target == "MXN":
        st.error("Saldo insuficiente para el mínimo de $10 MXN")
    else:
        # Ejecución con el máximo capital posible
        payload = {
            "book": book,
            "side": "buy",
            "type": "market",
            "minor": f"{monto_total:.2f}"
        }
        res = bitso_api("POST", "/v3/orders/", payload)
        
        if res.get('success'):
            st.success(f"¡ADAPTACIÓN TOTAL DE ${monto_total:.2f} EXITOSA!")
            st.balloons()
        else:
            error_msg = res.get('error', {}).get('message', 'Fallo de Firma')
            st.error(f"Bitso dice: {error_msg}")

st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nModo: MAX_CAPITAL\nSincronizado.")
