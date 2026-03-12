import streamlit as st
import time, requests, hashlib, hmac, os
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CONFIGURACIÓN ---
API_KEY = st.secrets.get("BITSO_API_KEY") or os.getenv("BITSO_API_KEY")
API_SECRET = st.secrets.get("BITSO_API_SECRET") or os.getenv("BITSO_API_SECRET")

st.set_page_config(layout="wide", page_title="ANGEL IA | NEURAL TERMINAL")

# --- ESTILO MORADO NEÓN HOLLYWOOD ---
st.markdown("""
    <style>
    .stApp { background: #05000a; color: #bc00ff; font-family: 'Courier New', monospace; }
    .stMetric { background: rgba(30, 0, 60, 0.4); border: 1px solid #bc00ff; border-radius: 15px; box-shadow: 0 0 15px #bc00ff; }
    h1, h2, h3 { color: #bc00ff !important; text-shadow: 0 0 20px #bc00ff; text-align: center; }
    .log-container { 
        background: #0d001a; border: 1px solid #bc00ff; padding: 15px; 
        font-family: 'Courier New', monospace; color: #e0b0ff; height: 250px; overflow-y: scroll;
        box-shadow: inset 0 0 10px #bc00ff;
    }
    div[data-testid="stMetricValue"] { color: #00ffcc !important; font-family: 'Orbitron', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

class AngelAI:
    def __init__(self):
        self.base = "https://api.bitso.com/v3"
        self.markets = ["btc_mxn", "eth_mxn", "usd_mxn", "nvda_usd", "aapl_usd"]

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

bot = AngelAI()
st.markdown("<h1>💜 ANGEL IA: NEURAL TERMINAL v3.2 💜</h1>", unsafe_allow_html=True)

# --- CÁLCULO DE SALDO REAL (DINÁMICO) ---
saldos_reales = bot.get_balances()
total_mxn = 0.0
mensajes_ia = []
precio_usd_mxn = bot.get_ticker("usd_mxn") or 18.0

for s in saldos_reales:
    cant = float(s['total'])
    if cant > 0.000001: # Si tienes algo de esa moneda
        coin = s['currency'].lower()
        if coin == 'mxn':
            total_mxn += cant
        else:
            # Intentar convertir a pesos
            p = bot.get_ticker(f"{coin}_mxn")
            if p == 0: # Si no hay par directo con pesos, buscar en USD
                p_usd = bot.get_ticker(f"{coin}_usd")
                p = p_usd * precio_usd_mxn
            
            valor_en_pesos = cant * p
            total_mxn += valor_en_pesos
            if valor_en_pesos > 1: # Solo reportar lo que valga más de 1 peso
                mensajes_ia.append(f"Detectado {coin.upper()}: {cant:.4f} (~${valor_en_pesos:.2f} MXN)")

# --- DASHBOARD DE PRECIOS ---
col_precios = st.columns(len(bot.markets))
for i, m in enumerate(bot.markets):
    p = bot.get_ticker(m)
    with col_precios[i]:
        st.metric(m.split('_')[0].upper(), f"${p:,.2f}")

st.divider()

# --- MONITOR Y BITÁCORA ---
col_main, col_log = st.columns([2, 1])

with col_main:
    st.markdown("### 📈 ANALÍTICA DE MERCADO")
    # Gráfica estética
    df = pd.DataFrame({
        'Open': [precio_usd_mxn + (i*0.1) for i in range(30)],
        'High': [precio_usd_mxn + (i*0.2) for i in range(30)],
        'Low': [precio_usd_mxn - (i*0.1) for i in range(30)],
        'Close': [precio_usd_mxn + (i*0.15) for i in range(30)],
        'Volume': [100 for _ in range(30)]
    })
    df.index = pd.date_range(start=datetime.now(), periods=30, freq='H')
    mc = mpf.make_marketcolors(up='#bc00ff', down='#550088', inherit=True)
    s  = mpf.make_mpf_style(marketcolors=mc, gridcolor='#111', facecolor='#05000a', edgecolor='#bc00ff')
    buf = BytesIO()
    mpf.plot(df, type='candle', style=s, figratio=(16,8), savefig=dict(fname=buf, dpi=100))
    st.image(buf, use_container_width=True)

with col_log:
    st.markdown("### 🧠 PENSAMIENTO DE LA IA")
    log_html = '<div class="log-container">'
    log_html += f"<p>[{datetime.now().strftime('%H:%M')}] > IA: Sistema inicializado.</p>"
    for msg in mensajes_ia:
        log_html += f"<p style='color:#00ffcc'>[{datetime.now().strftime('%H:%M')}] > IA: {msg}</p>"
    log_html += f"<p style='color:#bc00ff'>[{datetime.now().strftime('%H:%M')}] > IA: Analizando rebalanceo con presupuesto de $20 MXN.</p>"
    log_html += "</div>"
    st.markdown(log_html, unsafe_allow_html=True)
    st.button("Manual Override: COMPRAR $20 MXN")

# --- PROGRESO REAL ---
st.divider()
meta_mxn = 10000 * precio_usd_mxn
progreso = min(total_mxn / meta_mxn, 1.0)

st.write(f"### AVANCE HACIA LA LIBERTAD: {progreso*100:.4f}%")
st.progress(progreso)
st.write(f"💳 SALDO TOTAL REAL: **${total_mxn:,.2f} MXN** | OBJETIVO: **${meta_mxn:,.2f} MXN**")
