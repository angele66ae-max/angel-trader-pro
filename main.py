import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CREDENCIALES ---
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

st.set_page_config(layout="wide", page_title="SHARK NEON v8")

# --- ESTILO NEÓN + EFECTO TIBURÓN ---
st.markdown("""
    <style>
    @keyframes shark-attack {
        0% { transform: translate(1px, 1px) rotate(0deg); background-color: #020205; }
        10% { transform: translate(-1px, -2px) rotate(-1deg); background-color: #ff000033; }
        20% { transform: translate(-3px, 0px) rotate(1deg); }
        30% { transform: translate(3px, 2px) rotate(0deg); }
        40% { transform: translate(1px, -1px) rotate(1deg); }
        50% { transform: translate(-1px, 2px) rotate(-1deg); background-color: #ff000066; }
        100% { transform: translate(1px, 1px) rotate(0deg); background-color: #020205; }
    }
    .shark-bite {
        animation: shark-attack 0.5s;
        animation-iteration-count: 1;
    }
    .stApp { background-color: #020205; color: #bc13fe; font-family: 'JetBrains Mono', monospace; }
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #00d4ff !important; text-shadow: 0 0 10px #bc13fe; }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #bc13fe, #00d4ff);
        box-shadow: 0 0 20px #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

def get_data():
    if not API_KEY or not API_SECRET: return None, "Faltan Credenciales"
    # FIX 404: Sin diagonal final
    base = "https://api.bitso.com"
    path = "/v3/balances" 
    
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

# --- HEADER ---
st.title("🦈 SHARK SYSTEM: NEON CORE v8.0")

balances, status = get_data()

if status == "OK":
    # ACTIVAR EFECTO TIBURÓN AL CARGAR
    st.markdown('<div class="shark-bite"></div>', unsafe_allow_html=True)
    
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
    
    # --- PROGRESO META $10,000 USD ---
    total_usd = total_mxn / p_usd
    progreso = min(total_usd / 10000.0, 1.0)

    st.subheader("💰 BILLETERA STARSHIP")
    st.table(pd.DataFrame(wallet_data))
    
    col1, col2 = st.columns(2)
    col1.metric("TOTAL NET WORTH", f"${total_mxn:,.2f} MXN")
    col2.metric("META USD", f"${total_usd:,.2f} / $10,000")
    
    st.write(f"**Nivel de Depredador:** {progreso*100:.2f}%")
    st.progress(progreso)
    
    if progreso >= 1.0:
        st.balloons()
        st.success("¡EL TIBURÓN HA COMIDO! META DE $10,000 USD ALCANZADA.")
else:
    st.error(f"⚠️ FALLO DE ENLACE: {status}")
    st.info("Revisa que no tengas una '/' al final de la URL en tu configuración.")

# --- GRÁFICA ---
st.divider()
st.subheader("📊 NEON STREAM ANALYSIS")
curr_btc = get_ticker("btc_mxn") or 1250000
df = pd.DataFrame({'Open': [curr_btc]*10, 'High': [curr_btc*1.01]*10, 'Low': [curr_btc*0.99]*10, 'Close': [curr_btc]*10})
df.index = pd.date_range(start=datetime.now(), periods=10, freq='H')
mc = mpf.make_marketcolors(up='#00f2ff', down='#bc13fe', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#1a1a3a', facecolor='#020205', edgecolor='#bc13fe')
buf = BytesIO()
mpf.plot(df, type='candle', style=s, figratio=(16,6), savefig=dict(fname=buf, dpi=100))
st.image(buf, use_container_width=True)
