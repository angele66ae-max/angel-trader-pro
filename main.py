import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CREDENCIALES ---
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

st.set_page_config(layout="wide", page_title="SHARK NEON v8.0")

# --- ESTILO + ANIMACIÓN ---
st.markdown("""
    <style>
    @keyframes shark-bite {
        0% { transform: scale(1); background-color: #020205; }
        10% { transform: scale(1.02) rotate(1deg); background-color: #ff000033; }
        50% { transform: scale(0.98) rotate(-1deg); background-color: #ff000055; }
        100% { transform: scale(1); background-color: #020205; }
    }
    .shark-effect {
        animation: shark-bite 0.5s ease-in-out;
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1;
        pointer-events: none;
    }
    .stApp { background-color: #020205; color: #bc13fe; font-family: 'JetBrains Mono', monospace; }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #bc13fe, #00d4ff);
        box-shadow: 0 0 20px #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

def get_data():
    if not API_KEY or not API_SECRET: return None, "Faltan Credenciales"
    base = "https://api.bitso.com"
    path = "/v3/balances" # SIN diagonal final para evitar 404
    
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + path
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    
    try:
        r = requests.get(base + path, headers=headers, timeout=10)
        if r.status_code == 200: return r.json()['payload']['balances'], "OK"
        return None, f"Error {r.status_code}"
    except Exception as e: return None, str(e)

def get_ticker(book):
    try:
        r = requests.get(f"https://api.bitso.com/v3/ticker/?book={book}").json()
        return float(r['payload']['last'])
    except: return 0.0

# --- EJECUCIÓN ---
balances, status = get_data()

# Si todo está bien, lanzamos el efecto visual
if status == "OK":
    st.markdown('<div class="shark-effect"></div>', unsafe_allow_html=True)

st.title("🦈 SHARK SYSTEM: NEON CORE v8.0")

if status == "OK":
    total_mxn = 0.0
    wallet_data = []
    p_usd = get_ticker("usd_mxn") or 18.00
    
    for b in balances:
        cant = float(b['total'])
        if cant > 0:
            coin = b['currency'].upper()
            price = 1.0 if coin == "MXN" else get_ticker(f"{coin.lower()}_mxn")
            v_mxn = cant * price
            total_mxn += v_mxn
            if v_mxn > 1.0:
                wallet_data.append({"TOKEN": coin, "CANTIDAD": cant, "VALOR": f"${v_mxn:,.2f}"})
    
    total_usd = total_mxn / p_usd
    progreso = min(total_usd / 10000.0, 1.0)
    
    col1, col2 = st.columns(2)
    col1.metric("NET WORTH", f"${total_mxn:,.2f} MXN")
    col2.metric("META USD", f"${total_usd:,.2f} / $10,000")
    
    st.write(f"**Progreso del Depredador:** {progreso*100:.2f}%")
    st.progress(progreso)
else:
    st.error(f"⚠️ FALLO DE ENLACE: {status}")

# --- GRÁFICA ---
st.divider()
st.subheader("📊 NEON STREAM ANALYSIS")
curr_btc = get_ticker("btc_mxn") or 1250000
df = pd.DataFrame({'Open': [curr_btc]*10, 'High': [curr_btc*1.01]*10, 'Low': [curr_btc*0.99]*10, 'Close': [curr_btc]*10})
df.index = pd.date_range(start=datetime.now(), periods=10, freq='H')

mc = mpf.make_marketcolors(up='#00f2ff', down='#bc13fe', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#0d1117', facecolor='#020205', edgecolor='#bc13fe')
buf = BytesIO()
mpf.plot(df, type='candle', style=s, figratio=(16,6), savefig=dict(fname=buf, dpi=100))
st.image(buf, use_container_width=True)
