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

balances =
