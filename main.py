import streamlit as st
import time, requests, hashlib, hmac, os
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()
API_KEY = st.secrets.get("BITSO_API_KEY") or os.getenv("BITSO_API_KEY")
API_SECRET = st.secrets.get("BITSO_API_SECRET") or os.getenv("BITSO_API_SECRET")

# --- DISEÑO CYBERPUNK REAL ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .stMetric { background-color: #080808; border: 1px solid #00FF41; border-radius: 10px; padding: 15px; box-shadow: 0 0 10px #00FF41; }
    h1 { text-shadow: 0 0 15px #00FF41; text-align: center; color: #00FF41 !important; }
    div[data-testid="stMetricValue"] { color: #00FF41 !important; font-size: 35px !important; }
    </style>
    """, unsafe_allow_html=True)

class BitsoEngine:
    def __init__(self):
        self.base = "https://api.bitso.com/v3"

    def sign(self, method, path, payload=""):
        nonce = str(int(time.time() * 1000))
        message = nonce + method + path + payload
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
        return {"Authorization": f"Bitso {API_KEY}:{nonce}:{signature}", "Content-Type": "application/json"}

    def get_ticker(self, book):
        try: return float(requests.get(f"{self.base}/ticker/?book={book}").json()['payload']['last'])
        except: return 0.0

    def get_real_balance(self):
        path = "/v3/balances/"
        headers = self.sign("GET", path)
        try:
            res = requests.get(f"https://api.bitso.com{path}", headers=headers).json()
            return res['payload']['balances']
        except: return []

# --- LÓGICA DE DATOS REALES ---
st.markdown("<h1>> ANGEL_IA_TERMINAL_</h1>", unsafe_allow_html=True)
bot = BitsoEngine()

# 1. Calcular Saldo Real Total
saldos = bot.get_real_balance()
total_mxn = 0.0
resumen_cartera = []

if saldos:
    for s in saldos:
        cant = float(s['total'])
        if cant > 0:
            coin = s['currency'].lower()
            if coin == 'mxn':
                total_mxn += cant
            else:
                precio = bot.get_ticker(f"{coin}_mxn")
                if precio > 0: total_mxn += (cant * precio)
            resumen_cartera.append(f"{coin.upper()}: {cant}")

# 2. Meta de $10k USD
precio_dolar = bot.get_ticker("usd_mxn") or 18.00
meta_mxn = 10000 * precio_dolar
progreso = min(total_mxn / meta_mxn, 1.0)

# --- INTERFAZ ---
st.metric(label="MI SALDO REAL TOTAL (MXN)", value=f"${total_mxn:,.2f}")
st.progress(progreso)
st.write(f"🎯 META: $10,000 USD (~${meta_mxn:,.2f} MXN)")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Billetera Activa")
    for item in resumen_cartera:
        st.write(f"🔹 {item}")

with col2:
    st.subheader("Acciones Rápidas")
    if st.button("EJECUTAR COMPRA BTC ($10)"):
        st.warning("Procesando orden real...")
        # Aquí iría la función de compra si los permisos están activos

st.divider()
st.markdown("<p style='text-align:center; color:#555;'>CONECTADO A BITSO MAINNET - 24/7</p>", unsafe_allow_html=True)
