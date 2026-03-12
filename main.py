import streamlit as st
import time
import requests
import hashlib
import hmac
import os
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from dotenv import load_dotenv

# 1. SEGURIDAD PRO (Secrets en Nube, .env en PC)
load_dotenv()
API_KEY = st.secrets.get("BITSO_API_KEY") or os.getenv("BITSO_API_KEY")
API_SECRET = st.secrets.get("BITSO_API_SECRET") or os.getenv("BITSO_API_SECRET")

# --- ESTILO "HACKER / PELÍCULA" (CSS ACTUALIZADO) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #00FF41;
        font-family: 'Courier New', Courier, monospace;
    }
    h1 {
        color: #00FF41 !important;
        text-shadow: 0 0 10px #00FF41;
        text-align: center;
    }
    .stMetric {
        background-color: #0d0d0d;
        border: 1px solid #00FF41;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 15px #00FF41;
    }
    div[data-testid="stMetricValue"] {
        color: #00FF41 !important;
    }
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: #00FF41;
        border: 2px solid #00FF41;
        border-radius: 20px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #00FF41;
        color: black;
        box-shadow: 0 0 20px #00FF41;
    }
    /* Estilo para el selector */
    div[data-testid="stSelectbox"] > div {
        background-color: #0d0d0d;
        border: 1px solid #00FF41;
        color: #00FF41;
    }
    </style>
    """, unsafe_allow_html=True)

class BitsoBot:
    def __init__(self):
        self.url_base = "https://api.bitso.com/v3"

    def firmar(self, metodo, endpoint, payload=""):
        nonce = str(int(time.time() * 1000))
        message = nonce + metodo + endpoint + payload
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
        return {"Authorization": f"Bitso {API_KEY}:{nonce}:{signature}", "Content-Type": "application/json"}

    def get_ticker(self, book):
        try:
            r = requests.get(f"{self.url_base}/ticker/?book={book}", timeout=5)
            return float(r.json()['payload']['last'])
        except: return None

    def get_saldo(self):
        endpoint = "/v3/balances/"
        headers = self.firmar("GET", endpoint)
        try:
            r = requests.get(f"https://api.bitso.com{endpoint}", headers=headers, timeout=5)
            return r.json()['payload']['balances']
        except: return []

    def get_candlesticks(self, book):
        # Bitso no tiene endpoint público de velas, usamos un proxy público confiable
        # Esto obtiene datos de los últimos 2 días en velas de 30 mins
        url = f"https://api.cryptowat.ch/markets/bitso/{book}/ohlc?periods=1800&after={int(time.time()) - 172800}"
        try:
            r = requests.get(url, timeout=10)
            data = r.json()['result']['1800']
            df = pd.DataFrame(data, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'N'])
            df['Time'] = pd.to_datetime(df['Time'], unit='s')
            df.set_index('Time', inplace=True)
            return df
        except Exception as e:
            return None

# --- INICIALIZACIÓN ---
st.markdown("<h1>> ANGEL_TRADER_IA_v2.0_</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
bot = BitsoBot()

# --- SIDEBAR (CONFIGURACIÓN) ---
st.sidebar.markdown("<h2 style='color:#00FF41;'>SELECCIÓN_MERCADO</h2>", unsafe_allow_html=True)
moneda = st.sidebar.selectbox(
    "Elije la cripto o divisa a operar:",
    ("btc_mxn", "eth_mxn", "xrp_mxn", "usd_mxn")
)
nombre_moneda = moneda.split('_')[0].upper()

# --- PANEL PRINCIPAL (PRECIO Y GRÁFICA) ---
precio = bot.get_ticker(moneda)
col1, col2 = st.columns([1, 2])

with col1:
    if precio:
        st.metric(label=f"💰 PRECIO_{nombre_moneda}_MXN", value=f"${precio:,.2f}")
    else:
        st.error("SISTEMA_ERROR: CONEXIÓN_FALLIDA")
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.toggle("🤖 ACTIVAR_MODO_AUTO_SCALPING", value=False)
    st.button("⚡ COMPRA_RÁPIDA ($10 MXN)")

with col2:
    st.write("📊 GRÁFICA_VELAS_JAPONESAS (PRO)")
    with st.spinner("💾 DESENCRIPTANDO DATOS DEL MERCADO..."):
        df_velas = bot.get_candlesticks(moneda)
        if df_velas is not None and not df_velas.empty:
            # Configuración profesional de mplfinance (colores neón)
            colores_hack = mpf.make_marketcolors(up='#00FF41', down='#FF003C', inherit=True)
            estilo_hack = mpf.make_mpf_style(marketcolors=colores_hack, gridcolor='#0d0d0d', facecolor='black', edgecolor='#00FF41')
            
            # Renderizar la gráfica como imagen en memoria
            buf = BytesIO()
            mpf.plot(df_velas, type='candle', style=estilo_hack, volume=True, figratio=(16, 9), figscale=1.2, savefig=dict(fname=buf, dpi=100))
            st.image(buf)
        else:
            st.error("Error al cargar datos gráficos.")

st.divider()

# --- SECCIÓN DE META (THE ROAD TO $10K USD) ---
st.markdown("<h2 style='text-align:center; color:#D4AF37;'>THE_ROAD_TO_10K_USD</h2>", unsafe_allow_html=True)

# Obtenemos saldos reales
saldos = bot.get_saldo()
total_mxn_estimado = 0
precio_usd_mxn = bot.get_ticker("usd_mxn") or 17.50 # Precio estimado si falla el ticker

if saldos:
    for s in saldos:
        currency = s['currency'].upper()
        amount = float(s['total'])
        if amount > 0:
            if currency == 'MXN':
                total_mxn_estimado += amount
            else:
                precio_moneda = bot.get_ticker(f"{currency.lower()}_mxn")
                if precio_moneda:
                    total_mxn_estimado += (amount * precio_moneda)

# Convertimos meta a pesos
meta_usd = 10000
meta_mxn = meta_usd * precio_usd_mxn
progreso = min(total_mxn_estimado / meta_mxn, 1.0) if meta_mxn > 0 else 0

st.progress(progreso)
st.metric(label="MI SALDO ESTIMADO (TOTAL_MXN)", value=f"${total_mxn_estimado:,.2f}", delta=f"Faltan ${max(meta_mxn - total_mxn_estimado, 0):,.2f}")

# Simulación de Ganancias Proyectadas (Chido)
col3, col4 = st.columns(2)
with col3:
    st.metric("GANANCIA HOY (SIMULADO)", "$150.00 MXN", "+0.1%")
with col4:
    st.metric("GANANCIA MES (SIMULADO)", "$3,200.00 MXN", "+2.5%")

st.markdown("<h4 style='text-align:center; color:white30;'>OPERANDO 24/7 EN LA BLOCKCHAIN</h4>", unsafe_allow_html=True)
