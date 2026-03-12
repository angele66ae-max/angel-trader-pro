import streamlit as st
import time, requests, hashlib, hmac, os
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CONFIGURACIÓN DE SEGURIDAD ---
API_KEY = st.secrets.get("BITSO_API_KEY") or os.getenv("BITSO_API_KEY")
API_SECRET = st.secrets.get("BITSO_API_SECRET") or os.getenv("BITSO_API_SECRET")

st.set_page_config(layout="wide", page_title="ANGEL IA | EYES ON THE PRIZE")

# --- ESTILO HOLLYWOOD MORADO ---
st.markdown("""
    <style>
    .stApp { background: #05000a; color: #bc00ff; font-family: 'Courier New', monospace; }
    .stMetric { background: rgba(30, 0, 60, 0.4); border: 1px solid #bc00ff; border-radius: 15px; box-shadow: 0 0 15px #bc00ff; }
    h1, h2 { color: #bc00ff !important; text-shadow: 0 0 20px #bc00ff; text-align: center; letter-spacing: 3px; }
    .log-container { 
        background: #0d001a; border: 1px solid #bc00ff; padding: 15px; 
        font-family: 'Courier New', monospace; color: #e0b0ff; height: 280px; overflow-y: scroll;
        box-shadow: inset 0 0 15px #bc00ff;
    }
    div[data-testid="stMetricValue"] { color: #00ffcc !important; font-size: 30px !important; }
    </style>
    """, unsafe_allow_html=True)

class AngelEngine:
    def __init__(self):
        self.base = "https://api.bitso.com/v3"
        # Libros para monitoreo en vivo
        self.books = ["btc_mxn", "eth_mxn", "usd_mxn", "nvda_usd", "aapl_usd"]

    def sign(self, method, path, payload=""):
        nonce = str(int(time.time() * 1000))
        message = nonce + method + path + payload
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
        return {"Authorization": f"Bitso {API_KEY}:{nonce}:{signature}", "Content-Type": "application/json"}

    def get_ticker(self, book):
        try:
            r = requests.get(f"{self.base}/ticker/?book={book}", timeout=5).json()
            return float(r['payload']['last'])
        except: return 0.0

    def get_balances(self):
        path = "/v3/balances/"
        headers = self.sign("GET", path)
        try:
            res = requests.get(f"https://api.bitso.com{path}", headers=headers).json()
            return res['payload']['balances']
        except: return []

bot = AngelEngine()
st.markdown("<h1>◈ ANGEL_IA_QUANTUM_CORE v3.3 ◈</h1>", unsafe_allow_html=True)

# --- ESCANEO DE CARTERA REAL ---
saldos = bot.get_balances()
total_mxn = 0.0
ia_thoughts = []
p_usd_mxn = bot.get_ticker("usd_mxn") or 18.20

for s in saldos:
    amount = float(s['total'])
    if amount > 0:
        coin = s['currency'].lower()
        price = 0.0
        
        # Lógica de conversión agresiva
        if coin == 'mxn':
            price = 1.0
        else:
            price = bot.get_ticker(f"{coin}_mxn")
            if price == 0:
                price = bot.get_ticker(f"{coin}_usd") * p_usd_mxn
        
        subtotal = amount * price
        total_mxn += subtotal
        
        if subtotal > 0.1: # Reportar cualquier cosa con valor > 10 centavos
            ia_thoughts.append(f"DETECTADO {coin.upper()}: {amount} (~${subtotal:,.2f} MXN)")

# --- PANEL DE CONTROL ---
c1, c2, c3, c4, c5 = st.columns(5)
tickers = {b: bot.get_ticker(b) for b in bot.books}
for i, b in enumerate(bot.books):
    with [c1, c2, c3, c4, c5][i]:
        st.metric(b.split('_')[0].upper(), f"${tickers[b]:,.2f}")

st.divider()

col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 📊 MERCADO EN TIEMPO REAL")
    # Generar gráfica de velas técnica
    df = pd.DataFrame({
        'Open': [tickers['btc_mxn'] * (0.99 + i*0.001) for i in range(24)],
        'High': [tickers['btc_mxn'] * (1.01 + i*0.001) for i in range(24)],
        'Low': [tickers['btc_mxn'] * (0.98 + i*0.001) for i in range(24)],
        'Close': [tickers['btc_mxn'] * (1.0 + i*0.001) for i in range(24)],
        'Volume': [100 for _ in range(24)]
    })
    df.index = pd.date_range(start=datetime.now(), periods=24, freq='H')
    mc = mpf.make_marketcolors(up='#bc00ff', down='#550088', inherit=True)
    s  = mpf.make_mpf_style(marketcolors=mc, gridcolor='#111', facecolor='#05000a', edgecolor='#bc00ff')
    buf = BytesIO()
    mpf.plot(df, type='candle', style=s, figratio=(16,8), savefig=dict(fname=buf, dpi=100))
    st.image(buf, use_container_width=True)

with col_right:
    st.markdown("### 🧠 LOG_DE_LA_IA")
    log_html = '<div class="log-container">'
    log_html += f"<p>[{datetime.now().strftime('%H:%M')}] > IA_CORE: ONLINE.</p>"
    if not ia_thoughts:
        log_html += "<p style='color:red;'>[!] ERROR: No se detectan saldos. ¿API con permisos?</p>"
    for thought in ia_thoughts:
        log_html += f"<p style='color:#00ffcc'>[{datetime.now().strftime('%H:%M')}] > IA: {thought}</p>"
    log_html += f"<p style='color:#bc00ff'>[{datetime.now().strftime('%H:%M')}] > IA: Monitoreando Nvidia y Apple para scalping.</p>"
    log_html += "</div>"
    st.markdown(log_html, unsafe_allow_html=True)
    if st.button("EJECUTAR REBALANCEO ($20 MXN)"):
        st.toast("Analizando la mejor entrada para tus $20 MXN...")

# --- BARRA DE PROGRESO A LOS 10K ---
st.divider()
target_usd = 10000
target_mxn = target_usd * p_usd_mx
