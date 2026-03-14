import streamlit as st
import pandas as pd
import numpy as np
import time
import hmac
import hashlib
import requests
from datetime import datetime

# --- CONFIGURACIÓN DE NÚCLEO PROFESIONAL ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: REAL TRADING")

# --- CREDENCIALES DE SEGURIDAD (PON TUS LLAVES AQUÍ) ---
# Sin estas llaves, el bot no puede generar dinero real.
BITSO_API_KEY = "TU_API_KEY_AQUI"
BITSO_API_SECRET = "TU_API_SECRET_AQUI"

# --- ESTÉTICA SHARK AI + FONDO MAHAGA (RECUPERADO) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), url("{fondo_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .card {{
        background: rgba(16, 22, 26, 0.95);
        border: 1px solid rgba(0, 242, 255, 0.6);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 242, 255, 0.2);
    }}
    .metric-title {{ color: #e0e0e0; font-size: 14px; font-weight: bold; }}
    .metric-value {{ color: #00f2ff; font-size: 28px; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }}
    .status-active {{ color: #00ff00; font-weight: bold; animation: blinker 1.5s linear infinite; }}
    @keyframes blinker {{ 50% {{ opacity: 0; }} }}
</style>
""", unsafe_allow_html=True)
# --- MOTOR DE CONEXIÓN REAL CON BITSO ---
def get_bitso_data(path):

    if BITSO_API_KEY == "TU_API_KEY_AQUI":
        return None

    nonce = str(int(time.time() * 1000))

    message = nonce + "GET" + path

    signature = hmac.new(
        BITSO_API_SECRET.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    auth_header = f"Bitso {BITSO_API_KEY}:{nonce}:{signature}"

    headers = {
        "Authorization": auth_header
    }

    response = requests.get(
        f"https://api.bitso.com{path}",
        headers=headers
    )

    return response.json()
