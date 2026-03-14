import streamlit as st
import time, hashlib, hmac, json, requests
import numpy as np

# --- CONFIGURACIÓN TÁCTICA DEL CENTRO DE PRESTIGIO ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: ADAPTATION", page_icon="⛩️")

# URL DE TU IMAGEN (Ya configurado para el fondo)
# Nota: Streamlit necesita una URL de imagen pública directa para el fondo
URL_FONDO_CÓSMICO = "https://i.ibb.co/hRt2W6V/mahoraga-cosmic-crown.png" 

# --- ESTILO VISUAL "MULTI-ADAPTACIÓN" ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=JetBrains+Mono&display=swap');
    
    .stApp {{
        background-color: #000000;
        background-image: url('{URL_FONDO_CÓSMICO}');
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
    }}

    /* Capa de contraste para legibilidad sobre el fondo cósmico */
    .stApp::before {{
        content: "";
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.4); z-index: -1;
    }}

    /* Tarjetas de Métricas estilo "Prestige" */
    .metric-card {{
        background: rgba(10, 10, 10, 0.9);
        border: 2px solid rgba(0, 242, 255, 0.2);
        border-radius: 12px;
        padding: 22px;
        backdrop-filter: blur(10px);
        text-align: center;
    }}

    /* Estilo para los logs de la IA */
    .ai-logs {{
        background: rgba(0, 0, 0, 0.95);
        border: 2px solid #00ff00;
        border-radius: 8px;
        padding: 15px;
        height: 350px;
        overflow-y: auto;
        color: #00ff00;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
    }}

    /* Botón DEPLOY Táctico */
    .stButton>button {{
        background: linear-gradient(135deg, #004d4d 0%, #001a1a 100%);
        color: #00f2ff !important;
        border: 1px solid #00f2ff !important;
        border-radius: 8px;
        width: 100%;
        font-family: 'Orbitron', sans-serif;
    }}
</style>
""", unsafe_allow_html=True)

# --- NÚCLEO DE CONEXIÓN BITSO (Criptos) ---
def bitso_api(method, path, payload=None):
    try:
        API_KEY = st.secrets["BITSO_API_KEY"]
        API_SECRET = st.secrets["BITSO_API_SECRET"]
        nonce = str(int(time.time() * 1000))
        json_payload = json.dumps(payload) if payload else ""
        message = nonce + method + path + json_payload
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}', 'Content-Type': 'application/json'}
        url = f"https://api.bitso.com{path}"
        if method == "POST": return requests.post(url, headers=headers, data=json_payload).json()
        return requests.get(url, headers=headers).json()
    except: return None

# --- OBTENER DATOS REALES (Bitso) ---
# Aquí integrarías Alpaca/Yahoo Finance para acciones
try:
    ticker = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()['payload']
    precio_real = float(ticker['last'])
    balance_data = bitso_api("GET", "/v3/balance")
    usd_real = next((i['available'] for i in balance_data
