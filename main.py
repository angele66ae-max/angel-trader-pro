import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="SHARK NEON v8.0")

# --- CREDENCIALES ---
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

# --- ESTILO NEÓN + EFECTO MORDIDA ---
st.markdown("""
    <style>
    /* Efecto de ataque de tiburón */
    @keyframes shark-bite {
        0% { transform: scale(1); background-color: #020205; }
        10% { transform: scale(1.05) rotate(1deg); background-color: #ff000044; }
        30% { transform: scale(0.95) rotate(-1deg); background-color: #ff000022; }
        100% { transform: scale(1); background-color: #020205; }
    }
    .shark-attack { animation: shark-bite 0.6s ease-out; }
    
    .stApp { background-color: #020205; color: #bc13fe; font-family: 'JetBrains Mono', monospace; }
    h1 { color: #00d4ff !important; text-shadow: 0 0 15px #bc13fe; }
    
    /* Barra de progreso Neón */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #bc13fe, #00d4ff);
        box-shadow: 0 0 20px #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

def get_data():
    if not API_KEY or not API_SECRET: return None, "Faltan Credenciales"
    # FIX 404: Se eliminó cualquier diagonal o punto extra en el path
    base = "https://api.bitso.com"
    path = "/v3/balances" 
    
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + path
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    
    try:
        r = requests.get(base + path, headers=headers, timeout=10)
        if r.status_code == 200: return r.json()['payload']['balances'], "OK"
        return None, f"Error {r.status_code}: Not Found"
    except Exception as e: return None, str(e)

def get_ticker(book):
    try:
        r = requests.get(f"https://api.bitso.com/v3/ticker/?book={book}").json()
        return float(r['payload']['last'])
    except: return 0.0

# --- LÓGICA DE INTERFAZ ---
balances, status = get_data()

# Si los datos cargan, se activa la animación de mordida
if status == "OK":
    st.markdown('<div class="shark-attack"></div>', unsafe_allow_html=True)

st.title("🦈 SHARK SYSTEM: NEON CORE v8.0")

if status == "OK":
    total_mxn = 0.0
    wallet_data = []
    p_usd = get_ticker("usd_mxn") or 17.82
    
    for b in balances:
        cant = float(b['total'])
        if cant > 0:
            coin = b['currency'].upper()
            price = 1.0 if coin == "MXN" else get_ticker(f"{coin.lower()}_mxn")
            v_mxn = cant * price
            total_mxn += v_mxn
            if v_mxn > 0.01:
                wallet_data.append({"TOKEN": coin, "CANTIDAD": cant, "VALOR": f"${v_mxn:,.2f}"})
    
    # PROGRESO HACIA META $10,000 USD
    total_usd = total_mxn / p_usd
    progreso = min(total_usd / 10000.0, 1.0)
    
    col1, col2 = st.columns(2)
    col1.metric("NET WORTH", f"${total_mxn:,.2f} MXN")
    col2.metric("META USD", f"${total_usd:,.2f} / $10,000")
    
    st.write(f"**Nivel de Voracidad:** {progreso*100:.2f}%")
    st.progress(progreso)
    st.table(pd.DataFrame(wallet_data))
else:
    # Instrucciones de reparación basadas en tus capturas
    st.error(f"⚠️ {status}")
    st.info("Revisa en Bitso: 1. Permiso 'Consultar Saldos' activo. 2. NO tener IPs registradas (Whitelist vacía).")

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
