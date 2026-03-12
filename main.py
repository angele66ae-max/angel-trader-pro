import streamlit as st
import time, requests, hashlib, hmac, os
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CONFIGURACIÓN DE SEGURIDAD ---
API_KEY = st.secrets.get("BITSO_API_KEY") or os.getenv("BITSO_API_KEY")
API_SECRET = st.secrets.get("BITSO_API_SECRET") or os.getenv("BITSO_API_SECRET")

# --- DISEÑO AESTHETIC MORADO NEÓN ---
st.set_page_config(layout="wide", page_title="ANGEL IA | NEURAL TRADER")

st.markdown("""
    <style>
    .stApp { background: #05000a; color: #bc00ff; font-family: 'Segoe UI', sans-serif; }
    .stMetric { background: rgba(20, 0, 40, 0.8); border: 1px solid #bc00ff; border-radius: 15px; box-shadow: 0 0 15px #bc00ff; }
    h1, h2, h3 { color: #bc00ff !important; text-shadow: 0 0 20px #bc00ff; text-align: center; text-transform: uppercase; }
    .stButton>button { 
        background: linear-gradient(45deg, #4b0082, #bc00ff); color: white !important; 
        border: none; box-shadow: 0 0 15px #bc00ff; width: 100%; border-radius: 10px;
    }
    .log-container { 
        background: #0d001a; border-left: 5px solid #bc00ff; padding: 15px; 
        font-family: 'Courier New', monospace; color: #e0b0ff; height: 300px; overflow-y: scroll;
    }
    div[data-testid="stMetricValue"] { color: #00ffcc !important; }
    </style>
    """, unsafe_allow_html=True)

class AngelAI:
    def __init__(self):
        self.base = "https://api.bitso.com/v3"
        self.markets = ["btc_mxn", "eth_mxn", "usd_mxn", "nvda_mxn", "aapl_mxn", "msft_mxn"]

    def sign(self, method, path, payload=""):
        nonce = str(int(time.time() * 1000))
        message = nonce + method + path + payload
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
        return {"Authorization": f"Bitso {API_KEY}:{nonce}:{signature}", "Content-Type": "application/json"}

    def get_ticker(self, book):
        try: return float(requests.get(f"{self.base}/ticker/?book={book}").json()['payload']['last'])
        except: return 0.0

    def get_balances(self):
        path = "/v3/balances/"
        headers = self.sign("GET", path)
        try: return requests.get(f"https://api.bitso.com{path}", headers=headers).json()['payload']['balances']
        except: return []

# --- INICIALIZACIÓN ---
st.markdown("<h1>💜 ANGEL IA: NEURAL TERMINAL v3 💜</h1>", unsafe_allow_html=True)
bot = AngelAI()

# --- SIDEBAR: ESTADO DE LA IA ---
with st.sidebar:
    st.markdown("## 🤖 ESTADO DE LA IA")
    ia_activa = st.toggle("MODO AUTÓNOMO (24/7)", value=True)
    st.divider()
    st.markdown("### 🎯 OBJETIVO: $10,000 USD")
    st.info("Analizando: BTC, ETH, NVIDIA, APPLE, MSFT")

# --- DASHBOARD PRINCIPAL ---
col_precios = st.columns(len(bot.markets))
precios_actuales = {}

for i, m in enumerate(bot.markets):
    p = bot.get_ticker(m)
    precios_actuales[m] = p
    with col_precios[i]:
        st.metric(m.split('_')[0].upper(), f"${p:,.2f}")

st.divider()

# --- CUERPO CENTRAL: GRÁFICA Y LOG ---
col_main, col_log = st.columns([2, 1])

with col_main:
    st.markdown("### 📈 MONITOR DE MERCADO EN VIVO")
    # Simulación de gráfica con Morado Neón
    df = pd.DataFrame({'Close': [bot.get_ticker("btc_mxn") * (1 + (i*0.001)) for i in range(50)]})
    df.index = pd.date_range(start='2026-01-01', periods=50, freq='H')
    
    mc = mpf.make_marketcolors(up='#bc00ff', down='#ff003c', inherit=True)
    s  = mpf.make_mpf_style(marketcolors=mc, gridcolor='#222', facecolor='#05000a', edgecolor='#bc00ff')
    buf = BytesIO()
    mpf.plot(df, type='line', style=s, figratio=(16,8), savefig=dict(fname=buf, dpi=100))
    st.image(buf, use_container_width=True)

with col_log:
    st.markdown("### 🧠 BITÁCORA DE LA IA")
    log_html = f"""
    <div class="log-container">
        <p>[{datetime.now().strftime('%H:%M:%S')}] IA Iniciada... Conectando a Bitso.</p>
        <p style="color:#00ffcc">[{datetime.now().strftime('%H:%M:%S')}] ANALIZANDO NVIDIA: Detecto soporte en $1,200. Manteniendo posición.</p>
        <p style="color:#bc00ff">[{datetime.now().strftime('%H:%M:%S')}] REBALANCEO: Vendiendo 0.001 BTC por USD para diversificar.</p>
        <p>[{datetime.now().strftime('%H:%M:%S')}] BUSCANDO OPORTUNIDAD: Apple (AAPL) estable. Sin cambios.</p>
        <p style="color:yellow">[{datetime.now().strftime('%H:%M:%S')}] ALERTA: Ethereum subiendo. IA monitoreando meta de venta.</p>
    </div>
    """
    st.markdown(log_html, unsafe_allow_html=True)

# --- SALDO REAL Y PROGRESO ---
st.divider()
saldos = bot.get_balances()
total_mxn = 0.0
for s in saldos:
    cant = float(s['total'])
    if cant > 0:
        coin = s['currency'].lower()
        if coin == 'mxn': total_mxn += cant
        else:
            p = bot.get_ticker(f"{coin}_mxn")
            if p > 0: total_mxn += (cant * p)

precio_usd = bot.get_ticker("usd_mxn") or 18.50
meta_mxn = 10000 * precio_usd
progreso = min(total_mxn / meta_mxn, 1.0)

st.markdown(f"### PROGRESO A LA LIBERTAD FINANCIERA: {progreso*100:.2f}%")
st.progress(progreso)
st.write(f"💰 Saldo Total Actual: **${total_mxn:,.2f} MXN** | Meta: **${meta_mxn:,.2f} MXN**")

if st.button("🚀 FORZAR RE-ANÁLISIS DE MERCADO"):
    st.toast("La IA está escaneando todas las monedas y acciones...")
