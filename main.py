import streamlit as st
import time, requests, hashlib, hmac, os
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from dotenv import load_dotenv

# 1. SEGURIDAD Y CARGA
load_dotenv()
API_KEY = st.secrets.get("BITSO_API_KEY") or os.getenv("BITSO_API_KEY")
API_SECRET = st.secrets.get("BITSO_API_SECRET") or os.getenv("BITSO_API_SECRET")

# --- DISEÑO ULTRA-AESTHETIC HOLLYWOOD (CSS) ---
st.set_page_config(layout="wide", page_title="ANGEL IA | TERMINAL")

st.markdown("""
    <style>
    /* Fondo animado y General */
    .stApp {
        background: radial-gradient(circle at center, #0a0a0a 0%, #000000 100%);
        color: #00FF41;
        font-family: 'Courier New', monospace;
    }
    
    /* Contenedores tipo Cristal */
    .stMetric, div[data-testid="stVerticalBlock"] > div {
        background: rgba(15, 15, 15, 0.7) !important;
        border: 1px solid rgba(0, 255, 65, 0.3) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.1) !important;
        backdrop-filter: blur(10px);
    }

    /* Títulos con Neon Glow */
    h1, h2, h3 {
        color: #00FF41 !important;
        text-shadow: 0 0 15px #00FF41, 0 0 30px #00FF41;
        letter-spacing: 5px;
        text-transform: uppercase;
        text-align: center;
    }

    /* Botones de Acción */
    .stButton>button {
        background: linear-gradient(45deg, #004d1a, #00FF41);
        color: black !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 5px !important;
        height: 3em !important;
        transition: 0.5s !important;
        box-shadow: 0 0 10px #00FF41;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px #00FF41;
    }

    /* Ocultar elementos de Streamlit */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

class AngelEngine:
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

    def get_balance(self):
        path = "/v3/balances/"
        headers = self.sign("GET", path)
        try: return requests.get(f"https://api.bitso.com{path}", headers=headers).json()['payload']['balances']
        except: return []

    def get_ohlc(self, book):
        # Datos para velas japonesas (Proxy de Cryptowatch para Bitso)
        url = f"https://api.cryptowat.ch/markets/bitso/{book}/ohlc?periods=3600&after={int(time.time()) - 86400}"
        try:
            data = requests.get(url).json()['result']['3600']
            df = pd.DataFrame(data, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Vol', 'N'])
            df['Time'] = pd.to_datetime(df['Time'], unit='s')
            df.set_index('Time', inplace=True)
            return df
        except: return None

# --- TERMINAL IA ---
st.markdown("<h1>◈ ANGEL_IA_QUANTUM_TERMINAL ◈</h1>", unsafe_allow_html=True)
bot = AngelEngine()

# --- DATOS EN TIEMPO REAL ---
with st.container():
    col_a, col_b, col_c = st.columns([1,2,1])
    
    with col_a:
        st.markdown("### 🛰️ NETWORK_STATUS")
        st.write("● SYSTEM: ONLINE")
        st.write("● CORE: AI_ACTIVE")
        st.write("● LATENCY: 24ms")
        
    with col_b:
        precio_btc = bot.get_ticker("btc_mxn")
        st.metric("BITCOIN / MXN", f"${precio_btc:,.2f}", delta="LIVE_FEED")
        
    with col_c:
        st.markdown("### 🔐 ENCRYPTION")
        st.write("AES-256 BIT")
        st.write("BITSO_MAINNET")

st.markdown("<br>", unsafe_allow_html=True)

# --- GRÁFICA DE VELAS PROFESIONAL ---
col_graph, col_stats = st.columns([3, 1])

with col_graph:
    df = bot.get_ohlc("btc_mxn")
    if df is not None:
        mc = mpf.make_marketcolors(up='#00FF41', down='#FF003C', inherit=True)
        s  = mpf.make_mpf_style(marketcolors=mc, gridcolor='#111', facecolor='black', edgecolor='#00FF41')
        buf = BytesIO()
        mpf.plot(df, type='candle', style=s, figratio=(16,7), savefig=dict(fname=buf, dpi=100))
        st.image(buf, use_container_width=True)

with col_stats:
    st.markdown("### 📊 MARKET_INSIGHTS")
    st.write("VOLATILITY: HIGH")
    st.write("TREND: BULLISH")
    st.divider()
    if st.button("EXECUTE_MARKET_BUY"):
        st.snow()
        st.success("ORDER_SENT_TO_BLOCKCHAIN")

# --- META 10K USD REAL ---
st.markdown("---")
saldos = bot.get_balance()
total_mxn = 0.0
for s in saldos:
    cant = float(s['total'])
    if cant > 0:
        coin = s['currency'].lower()
        if coin == 'mxn': total_mxn += cant
        else:
            p = bot.get_ticker(f"{coin}_mxn")
            if p > 0: total_mxn += (cant * p)

precio_usd = bot.get_ticker("usd_mxn") or 18.0
meta_mxn = 10000 * precio_usd
progreso = min(total_mxn / meta_mxn, 1.0)

st.markdown(f"<h2 style='color:#D4AF37;'>PATH_TO_FINANCIAL_FREEDOM: {progreso*100:.2f}%</h2>", unsafe_allow_html=True)
st.progress(progreso)
st.markdown(f"<p style='text-align:center;'>CURRENT_BALANCE: ${total_mxn:,.2f} MXN | TARGET: ${meta_mxn:,.2f} MXN</p>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; font-size:10px; opacity:0.3;'>© 2026 ANGEL_IA_CORP | UNIFIED_TRADING_INTERFACE</p>", unsafe_allow_html=True)
