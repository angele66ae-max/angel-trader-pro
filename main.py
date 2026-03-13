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

# --- ESTILO RGB AVANZADO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    .stApp { background-color: #020205; color: #bc13fe; font-family: 'JetBrains Mono', monospace; }
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #00d4ff !important; text-shadow: 0 0 10px #bc13fe; }
    .status-box { background: rgba(20, 0, 40, 0.8); border: 2px solid #00d4ff; padding: 15px; border-radius: 10px; box-shadow: 0 0 15px #bc13fe; }
    .stMetric { background: rgba(0, 0, 0, 0.5); border: 1px solid #bc13fe; border-radius: 5px; padding: 10px; }
    /* Estilo para la barra de progreso */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #bc13fe, #00d4ff);
    }
    </style>
    """, unsafe_allow_html=True)

def get_data():
    if not API_KEY or not API_SECRET: return None, "Faltan Credenciales"
    
    # --- FIX 404: PATH SIN DIAGONAL FINAL ---
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

col_main, col_side = st.columns([2, 1])

with col_side:
    st.subheader("📡 SISTEMA")
    with st.container():
        st.markdown('<div class="status-box">', unsafe_allow_html=True)
        st.markdown("**ESTADO:** 🟢 OPERATIVO")
        st.markdown("**OBJETIVO:** ESCALADO A $10K USD")
        st.info("Monitoreo activo de activos y meta financiera.")
        st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    p_usd_mxn = get_ticker("usd_mxn") or 18.00
    m1, m2, m3 = st.columns(3)
    m1.metric("₿ BTC", f"${get_ticker('btc_mxn'):,.0f} MXN")
    m2.metric("Ξ ETH", f"${get_ticker('eth_mxn'):,.0f} MXN")
    m3.metric("🌐 USD/MXN", f"${p_usd_mxn:,.2f}")

    st.divider()
    
    # --- WALLET Y PROGRESO ---
    st.subheader("💰 BILLETERA STARSHIP")
    balances, status = get_data()
    total_mxn = 0.0

    if status == "OK":
        wallet_data = []
        for b in balances:
            cant = float(b['total'])
            if cant > 0:
                coin = b['currency'].upper()
                price = 1.0 if coin == "MXN" else get_ticker(f"{coin.lower()}_mxn")
                if price == 0: price = get_ticker(f"{coin.lower()}_usd") * p_usd_mxn
                v_mxn = cant * price
                total_mxn += v_mxn
                if v_mxn > 1.0:
                    wallet_data.append({"TOKEN": coin, "CANTIDAD": cant, "PESOS": f"${v_mxn:,.2f}"})
        
        st.table(pd.DataFrame(wallet_data))
        
        # --- CÁLCULO DE META ---
        total_usd = total_mxn / p_usd_mxn
        meta_usd = 10000.0
        progreso = min(total_usd / meta_usd, 1.0)
        
        col_net1, col_net2 = st.columns(2)
        col_net1.metric("TOTAL NET WORTH", f"${total_mxn:,.2f} MXN")
        col_net2.metric("VALOR EN USD", f"${total_usd:,.2f} USD")
        
        st.write(f"**Progreso hacia la meta de $10,000 USD:** {progreso*100:.2f}%")
        st.progress(progreso)
        
    else:
        st.error(f"FALLO DE ENLACE: {status}")
        st.info("Verifica que el path sea '/v3/balances' y que tu API Key tenga permisos de lectura.")

# --- GRÁFICA ---
st.divider()
st.subheader("📊 NEON STREAM ANALYSIS")
curr_btc = get_ticker("btc_mxn") or 1250000
df = pd.DataFrame({'Open': [curr_btc]*15, 'High': [curr_btc*1.002]*15, 'Low': [curr_btc*0.998]*15, 'Close': [curr_btc]*15})
df.index = pd.date_range(start=datetime.now(), periods=15, freq='H')
mc = mpf.make_marketcolors(up='#00f2ff', down='#bc13fe', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#1a1a3a', facecolor='#020205', edgecolor='#bc13fe')
buf = BytesIO()
mpf.plot(df, type='candle', style=s, figratio=(16,6), savefig=dict(fname=buf, dpi=100))
st.image(buf, use_container_width=True)
