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

# --- ESTILO HOLLYWOOD MORADO ---
st.markdown("""
    <style>
    .stApp { background: #05000a; color: #bc00ff; font-family: 'Courier New', monospace; }
    .stMetric { background: rgba(30, 0, 60, 0.4); border: 1px solid #bc00ff; border-radius: 15px; box-shadow: 0 0 15px #bc00ff; }
    h1, h2 { color: #bc00ff !important; text-shadow: 0 0 20px #bc00ff; text-align: center; }
    .log-container { 
        background: #0d001a; border: 1px solid #bc00ff; padding: 15px; 
        font-family: 'Courier New', monospace; color: #e0b0ff; height: 300px; overflow-y: scroll;
        box-shadow: inset 0 0 15px #bc00ff;
    }
    div[data-testid="stMetricValue"] { color: #00ffcc !important; font-size: 28px !important; }
    </style>
    """, unsafe_allow_html=True)

class AngelEngine:
    def __init__(self):
        self.base = "https://api.bitso.com/v3"
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
            r = requests.get(f"https://api.bitso.com{path}", headers=headers).json()
            if 'payload' in r: return r['payload']['balances'], "OK"
            return [], f"Error Bitso: {r.get('error', {}).get('message', 'Desconocido')}"
        except Exception as e:
            return [], f"Error de Conexión: {str(e)}"

bot = AngelEngine()
st.markdown("<h1>◈ ANGEL_IA_QUANTUM_CORE v3.4 ◈</h1>", unsafe_allow_html=True)

# --- PROCESAMIENTO DE DATOS ---
p_usd_mxn = bot.get_ticker("usd_mxn") or 18.50 # Arreglado el nombre aquí
saldos_raw, status_ia = bot.get_balances()
total_mxn = 0.0
ia_log = []

if status_ia == "OK":
    for s in saldos_raw:
        amount = float(s['total'])
        if amount > 0:
            coin = s['currency'].lower()
            # Lógica de conversión
            if coin == 'mxn': p = 1.0
            else:
                p = bot.get_ticker(f"{coin}_mxn")
                if p == 0: p = bot.get_ticker(f"{coin}_usd") * p_usd_mxn
            
            valor = amount * p
            total_mxn += valor
            if valor > 0.1:
                ia_log.append(f"DETECTADO {coin.upper()}: {amount} (~${valor:,.2f} MXN)")
else:
    ia_log.append(f"⚠️ ALERTA: {status_ia}")

# --- INTERFAZ ---
cols = st.columns(len(bot.books))
for i, b in enumerate(bot.books):
    with cols[i]:
        st.metric(b.split('_')[0].upper(), f"${bot.get_ticker(b):,.2f}")

st.divider()

col_a, col_b = st.columns([2, 1])

with col_a:
    st.markdown("### 📊 VIGILANCIA DE MERCADO")
    # Gráfica estética (Velas moradas)
    df = pd.DataFrame({'Open': [10+i for i in range(20)], 'High': [12+i for i in range(20)], 
                       'Low': [9+i for i in range(20)], 'Close': [11+i for i in range(20)], 'Volume': [100]*20})
    df.index = pd.date_range(start=datetime.now(), periods=20, freq='H')
    mc = mpf.make_marketcolors(up='#bc00ff', down='#550088', inherit=True)
    s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#111', facecolor='#05000a', edgecolor='#bc00ff')
    buf = BytesIO(); mpf.plot(df, type='candle', style=s, figratio=(16,8), savefig=dict(fname=buf, dpi=100))
    st.image(buf, use_container_width=True)

with col_b:
    st.markdown("### 🧠 PENSAMIENTO IA")
    log_html = '<div class="log-container">'
    for line in ia_log:
        color = "#00ffcc" if "DETECTADO" in line else "#ff0066"
        log_html += f"<p style='color:{color};'>[{datetime.now().strftime('%H:%M')}] > {line}</p>"
    log_html += f"<p style='color:#bc00ff;'>[{datetime.now().strftime('%H:%M')}] > IA: Esperando orden de compra mínima ($100 MXN para trading en Bitso).</p>"
    log_html += "</div>"
    st.markdown(log_html, unsafe_allow_html=True)
    st.button("FORZAR ESCANEO DE RED")

# --- PROGRESO ---
st.divider()
meta_mxn = 10000 * p_usd_mxn # Nombre corregido p_usd_mxn
progreso = min(total_mxn / meta_mxn, 1.0) if meta_mxn > 0 else 0

st.markdown(f"### 🚀 OBJETIVO $10,000 USD: {progreso*100:.4f}%")
st.progress(progreso)
st.write(f"💵 SALDO REAL: **${total_mxn:,.2f} MXN** | TARGET: **${meta_mxn:,.2f} MXN**")
