import streamlit as st
import pandas as pd
import pandas_ta as ta
import requests
import hmac
import hashlib
import time
import json
from datetime import datetime

# --- 1. CONFIGURACIÓN PRO ---
st.set_page_config(layout="wide", page_title="MAHORA FULL AUTO")

# Credenciales (Asegúrate de que tengan permisos de 'Write' en Bitso)
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"
LIBROS = ["btc_mxn", "eth_mxn", "sol_mxn", "xrp_mxn"]

st.markdown("""
<style>
    .stApp { background: #000505; color: #39FF14; font-family: 'Courier New', monospace; }
    .log-box { background: #000; border: 1px solid #39FF14; padding: 15px; height: 300px; overflow-y: auto; }
    .status-live { color: #ff00ff; font-weight: bold; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# --- 2. FUNCIONES DE EJECUCIÓN REAL ---
def firmar_solicitud(metodo, path, payload=None):
    nonce = str(int(time.time() * 1000))
    json_payload = json.dumps(payload) if payload else ""
    message = nonce + metodo + path + json_payload
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    return {
        'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}',
        'Content-Type': 'application/json'
    }

def ejecutar_orden_real(book, side, amount_mxn):
    path = "/v3/orders/"
    payload = {
        "book": book,
        "side": side,
        "type": "market",
        "minor": f"{amount_mxn:.2f}" # Usamos 'minor' para especificar monto en MXN
    }
    headers = firmar_solicitud("POST", path, payload)
    r = requests.post(f"https://api.bitso.com{path}", headers=headers, json=payload)
    return r.json()

def obtener_datos_reales(book):
    # Obtenemos los últimos trades para generar indicadores reales, no random
    r = requests.get(f"https://api.bitso.com/v3/trades/?book={book}").json()
    trades = r['payload']
    df = pd.DataFrame(trades)
    df['price'] = df['price'].astype(float)
    # Cálculo de indicadores técnicos sobre trades reales
    df['rsi'] = ta.rsi(df['price'], length=14)
    df['sma7'] = ta.sma(df['price'], length=7)
    df['sma21'] = ta.sma(df['price'], length=21)
    return df, df['price'].iloc[0]

# --- 3. LÓGICA DE CONTROL Y SALDOS ---
def get_balances():
    path = "/v3/balance/"
    headers = firmar_solicitud("GET", path)
    r = requests.get(f"https://api.bitso.com{path}", headers=headers).json()
    return {b['currency'].upper(): float(b['total']) for b in r['payload']['balances']}

# --- 4. INTERFAZ Y PROCESAMIENTO ---
st.title("⛩️ MAHORASHARK: OPERATIVA REAL 10K")
bal = get_balances()
mxn_disponible = bal.get('MXN', 0)
btc_p = float(requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()['payload']['last'])
valor_usd
