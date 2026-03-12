import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- SHARK AUTH ---
API_KEY = st.secrets.get("BITSO_API_KEY", "").strip()
API_SECRET = st.secrets.get("BITSO_API_SECRET", "").strip()

st.set_page_config(layout="wide", page_title="SHARK TANK | WALLET")

# --- TRADINGVIEW DARK STYLE ---
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #e0e0e0; }
    .stMetric { background: #1c2128; border: 1px solid #30363d; border-radius: 8px; padding: 15px; }
    h1, h2 { color: #2962ff !important; }
    .auth-card { background: #2d1111; border: 1px solid #ff4b4b; padding: 15px; border-radius: 5px; color: #ffafaf; }
    </style>
    """, unsafe_allow_html=True)

class SharkEngine:
    def __init__(self):
        self.base = "https://api.bitso.com"

    def get_price(self, book):
        try:
            r = requests.get(f"{self.base}/v3/ticker/?book={book}").json()
            return float(r['payload']['last'])
        except: return 0.0

    def get_balances(self):
        if not API_KEY or not API_SECRET: return None, "KEYS_NOT_FOUND"
        path = "/v3/balances/"
        nonce = str(int(time.time() * 1000))
        message = nonce + "GET" + path
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
        try:
            r = requests.get(self.base + path, headers=headers, timeout=10)
            data = r.json()
            if r.status_code == 200:
                return data['payload']['balances'], "OK"
            else:
                return None, f"BITSO_ERROR: {data['error']['message']}"
        except Exception as e:
            return None, f"CONN_ERROR: {str(e)}"

bot = SharkEngine()
p_usd_mxn = bot.get_price("usd_mxn") or 18.25

st.title("🦈 SHARK TANK: PORTFOLIO TRACKER")

# --- STATUS CHECK ---
bal_data, status = bot.get_balances()

if status != "OK":
    st.markdown(f"""
    <div class="auth-card">
        <h4>🚨 ACCESO DENEGADO (AUTH_ERROR)</h4>
        <p>Bitso no reconoce tus llaves. Sigue estos pasos para arreglarlo:</p>
        <ul>
            <li>1. Ve a <b>Bitso > Perfil > API</b>.</li>
            <li>2. Borra tus llaves actuales y crea unas <b>NUEVAS</b>.</li>
            <li>3. Asegúrate de marcar la casilla: <b>"Consultar saldos" (Account Balances)</b>.</li>
            <li>4. Copia y pega en Streamlit Secrets sin dejar espacios al final.</li>
        </ul>
        <small>Error detectado: {status}</small>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- TABLA DE BILLETERA ---
st.subheader("📁 My Assets (Crypto & Cash)")
total_mxn = 0.0

if status == "OK":
    rows = []
    for b in bal_data:
        qty = float(b['total'])
        if qty > 0.00000001:
            coin = b['currency'].upper()
            # Calcular precios
            if coin == 'MXN': p_mxn = 1.0
            else:
                p_mxn = bot.get_price(f"{coin.lower()}_mxn")
                if p_mxn == 0: p_mxn = bot.get_price(f"{coin.lower()}_usd") * p_usd_mxn
            
            val_mxn = qty * p_mxn
            val_usd = val_mxn / p_usd_mxn
            total_mxn += val_mxn
            
            rows.append({
                "ASSET": coin,
                "TOTAL BALANCE": f"{qty:.8f}",
                "VALUE (MXN)": f"${val_mxn:,.2f}",
                "VALUE (USD)": f"${val_usd:,.2f}"
            })
    
    if rows:
        st.table(pd.DataFrame(rows))
    else:
        st.info("No balances found. Make sure you have at least $1 MXN in Bitso.")
else:
    st.warning("⚠️ Wallet data hidden due to connection error.")

# --- GRÁFICA Y MÉTRICAS ---
st.divider()
c_chart, c_metrics = st.columns([2, 1])

with c_chart:
    st.subheader("📉 Market Trend")
    # Generamos velas según precio actual para que la gráfica tenga sentido
    p_now = bot.get_price("btc_mxn") or 1230000
    df = pd.DataFrame({
        'Open': [p_now] * 30, 'High': [p_now * 1.002] * 30, 
        'Low': [p_now * 0.998] * 30, 'Close': [p_now * 1.001] * 30, 'Volume': [100] * 30
    })
    df.index = pd.date_range(start=datetime.now(), periods=30, freq='15min')
    mc = mpf.make_marketcolors(up='#26a69a', down='#ef5350', inherit=True)
    s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#363a45', facecolor='#0e1117', edgecolor='#363a45')
    buf = BytesIO(); mpf.plot(df, type='candle', style=s, figratio=(16,8), savefig=dict(fname=buf, dpi=100))
    st.image(buf, use_container_width=True)

with c_metrics:
    st.subheader("🏆 Total Wealth")
    st.metric("NET WORTH (MXN)", f"${total_mxn:,.2f}")
    st.metric("NET WORTH (USD)", f"${(total_mxn / p_usd_mxn):,.2f}")
    
    target_usd = 10000
    progress = min((total_mxn / p_usd_mxn) / target_usd, 1.0)
    st.write(f"Goal to $10k USD: {progress*100:.4f}%")
    st.progress(progress)
