import streamlit as st
import time
import requests
import hashlib
import hmac
import os
from dotenv import load_dotenv

# 1. Configuración de Seguridad
load_dotenv()
API_KEY = st.secrets.get("BITSO_API_KEY") or os.getenv("BITSO_API_KEY")
API_SECRET = st.secrets.get("BITSO_API_SECRET") or os.getenv("BITSO_API_SECRET")

# --- ESTILO "HACKER / PELÍCULA" (CSS) ---
st.markdown("""
    <style>
    .main {
        background-color: #000000;
    }
    .stApp {
        background-color: #000000;
    }
    h1 {
        color: #00FF41; /* Verde Matrix */
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 0 0 10px #00FF41;
        text-align: center;
    }
    .stMetric {
        background-color: #0d0d0d;
        border: 1px solid #00FF41;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 0 15px #00FF41;
    }
    div[data-testid="stMetricValue"] {
        color: #00FF41 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: #00FF41;
        border: 2px solid #00FF41;
        border-radius: 20px;
        font-weight: bold;
        text-transform: uppercase;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #00FF41;
        color: black;
        box-shadow: 0 0 20px #00FF41;
    }
    </style>
    """, unsafe_allow_html=True)

class AngelTrader:
    def __init__(self):
        self.url_base = "https://api.bitso.com"

    def firmar_solicitud(self, metodo, endpoint, payload=""):
        nonce = str(int(time.time() * 1000))
        message = nonce + metodo + endpoint + payload
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
        return {"Authorization": f"Bitso {API_KEY}:{nonce}:{signature}", "Content-Type": "application/json"}

    def obtener_precio(self):
        try:
            r = requests.get(f"{self.url_base}/v3/ticker/?book=btc_mxn")
            return float(r.json()['payload']['last'])
        except: return None

    def comprar_btc(self, monto_mxn):
        endpoint = "/v3/orders/"
        payload = f'{{"book":"btc_mxn","side":"buy","type":"market","major":"{monto_mxn}"}}'
        headers = self.firmar_solicitud("POST", endpoint, payload)
        try:
            r = requests.post(f"{self.url_base}{endpoint}", data=payload, headers=headers)
            return r.json()
        except Exception as e: return {"status": "error", "message": str(e)}

# --- INTERFAZ ---
st.markdown("<h1>> ANGEL_IA_OPERATIONS_</h1>", unsafe_allow_html=True)

bot = AngelTrader()

# Simulación de "Carga de Datos"
with st.status("📡 Conectando con los servidores de Bitso...", expanded=False) as status:
    precio = bot.obtener_precio()
    time.sleep(1)
    st.write("🔐 Autenticando llaves API...")
    time.sleep(1)
    status.update(label="✅ CONEXIÓN ESTABLECIDA", state="complete", expanded=False)

# El Ticker principal
if precio:
    st.metric(label="BITCOIN_PRICE_MXN", value=f"${precio:,.2f}")
else:
    st.error("SYSTEM_ERROR: CONNECTION_FAILED")

st.markdown("<br>", unsafe_allow_html=True)

# Botón de acción con estilo
if st.button("EJECUTAR ORDEN DE COMPRA (10 MXN)"):
    with st.spinner("💾 PROCESANDO TRANSACCIÓN EN LA BLOCKCHAIN..."):
        res = bot.comprar_btc("10.00")
        if "payload" in res:
            st.balloons()
            st.success(f"ORDEN COMPLETADA_ ID: {res['payload']['oid']}")
        else:
            st.error("ACCESO DENEGADO_ REVISA SALDO O LLAVES")

# Sidebar Cyberpunk
st.sidebar.markdown("<h2 style='color:#00FF41;'>MENU_SISTEMA</h2>", unsafe_allow_html=True)
ia_status = st.sidebar.toggle("AUTO_TRADING_MODE")

if ia_status:
    st.sidebar.warning("🤖 IA: BUSCANDO FALLAS EN EL MERCADO...")
