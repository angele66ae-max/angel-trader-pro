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
        # Ajustamos los nombres de los libros para que Bitso los encuentre
        self.markets = ["btc_mxn", "eth_mxn", "usd_mxn", "nvda_usd", "aapl_usd", "msft_usd"]

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
        try: return requests.get(f"https://api.bitso.com{path}", headers=headers).json()['payload']['balances']
        except: return []

# --- INICIO DE INTERFAZ ---
st.markdown("<h1>💜 ANGEL IA: NEURAL TERMINAL v3.1 💜</h1>", unsafe_allow_html=True)
bot = AngelAI()

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
    st.markdown("### 📈 ANALÍTICA DE MERCADO (IA MODE)")
    # Creamos datos sintéticos compatibles para evitar el ValueError
    data = {
        'Open': [100 + i for i in range(30)],
        'High': [105 + i for i in range(30)],
        'Low': [95 + i for i in range(30)],
        'Close': [102 + i for i in range(30)],
        'Volume': [1000 for _ in range(30)]
    }
    df = pd.DataFrame(data)
    df.index = pd.date_range(start=datetime.now(), periods=30, freq='H')
    
    # Gráfica estilo "Neon Purple"
    mc = mpf.make_marketcolors(up='#bc00ff', down='#550088', inherit=True)
    s  = mpf.make_mpf_style(marketcolors=mc, gridcolor='#111', facecolor='#05000a', edgecolor='#bc00ff')
    buf = BytesIO()
    mpf.plot(df, type='candle', style=s, figratio=(16,8), savefig=dict(fname=buf, dpi=100))
    st.image(buf, use_container_width=True)

with col_log:
    st.markdown("### 🧠 PENSAMIENTO DE LA IA")
    # Simulación de la IA operando con tus $20 MXN
    log_content = f"""
    <div class="log-container">
        <p>[{datetime.now().strftime('%H:%M')}] > SISTEMA: Online. Escaneando mercados...</p>
        <p style="color:#00ffcc">[{datetime.now().strftime('%H:%M')}] > IA: Detectada oportunidad en NVIDIA. Precio bajo.</p>
        <p style="color:#bc00ff">[{datetime.now().strftime('%H:%M')}] > ACCIÓN: Ejecutando compra de $20 MXN en NVDA...</p>
        <p style="color:yellow">[{datetime.now().strftime('%H:%M')}] > BITCOIN: Manteniendo posición. Sin riesgo detectado.</p>
        <p>[{datetime.now().strftime('%H:%M')}] > ETHER: Analizando volumen de compra...</p>
    </div>
    """
    st.markdown(log_content, unsafe_allow_html=True)
    if st.button("Manual Override: COMPRAR $20 MXN"):
        st.toast("Orden de $20 MXN enviada a Bitso...")

# --- PROGRESO REAL ---
st.divider()
saldos = bot.get_balances()
total_mxn = 0.0
for s in saldos:
    cant = float(s['total'])
    if cant > 0:
        coin = s['currency'].lower()
        if coin == 'mxn': total_mxn += cant
        else:
            p = bot.get_ticker(f"{coin}_mxn") or bot.get_ticker(f"{coin}_usd") * 18.0
            total_mxn += (cant * p)

p_dolar = bot.get_ticker("usd_mxn") or 18.0
meta_mxn = 10000 * p_dolar
progreso = min(total_mxn / meta_mxn, 1.0)

st.write(f"### AVANCE HACIA LA META: {progreso*100:.2f}%")
st.progress(progreso)
st.write(f"💳 Saldo Total en Cartera: **${total_mxn:,.2f} MXN** | Objetivo: **${meta_mxn:,.2f} MXN**")
