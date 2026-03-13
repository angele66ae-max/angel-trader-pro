import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="SHARK NEON v8.4")

# --- CREDENCIALES ---
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

# --- ESTILO SHARK AVANZADO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    
    .stApp { background-color: #020205; color: #bc13fe; font-family: 'JetBrains Mono', monospace; }
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #00d4ff !important; text-shadow: 0 0 10px #bc13fe; }
    .status-box { background: rgba(20, 0, 40, 0.8); border: 2px solid #00d4ff; padding: 15px; border-radius: 10px; box-shadow: 0 0 15px #bc13fe; }
    
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #bc13fe, #00d4ff);
        box-shadow: 0 0 15px #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

def get_data():
    if not API_KEY or not API_SECRET: return None, "Faltan Credenciales"
    
    # LA RUTA CRÍTICA: Añadimos la diagonal final que Bitso exige para tus permisos
    base = "https://api.bitso.com"
    path = "/v3/balances/" 
    
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

# --- HEADER Y MÉTRICAS RÁPIDAS ---
st.title("🦈 SHARK SYSTEM: NEON CORE v8.4")

p_usd = get_ticker("usd_mxn") or 17.83
m1, m2, m3 = st.columns(3)
m1.metric("₿ BTC", f"${get_ticker('btc_mxn'):,.0f} MXN")
m2.metric("Ξ ETH", f"${get_ticker('eth_mxn'):,.0f} MXN")
m3.metric("🌐 USD/MXN", f"${p_usd:,.2f}")

# --- CUERPO PRINCIPAL ---
col_main, col_sys = st.columns([2, 1])

balances, status = get_data()

with col_sys:
    st.subheader("📡 SISTEMA")
    estado_color = "🟢 OPERATIVO" if status == "OK" else "🔴 ERROR"
    st.markdown(f"""
    <div class="status-box">
        <b>ESTADO:</b> {estado_color}<br>
        <b>MOTOR:</b> SHARK-IA v8.4<br>
        <b>OBJETIVO:</b> $10,000 USD
    </div>
    """, unsafe_allow_html=True)
    
    if status != "OK":
        st.error(f"FALLO DE ENLACE: {status}")
        st.warning("Revisa que el API SECRET en Streamlit coincida con el de 'casa tiburones'.")

with col_main:
    if status == "OK":
        st.subheader("💰 BILLETERA STARSHIP")
        total_mxn = 0.0
        wallet_list = []
        
        for b in balances:
            cant = float(b['total'])
            if cant > 0:
                coin = b['currency'].upper()
                price = 1.0 if coin == "MXN" else get_ticker(f"{coin.lower()}_mxn")
                v_mxn = cant * price
                total_mxn += v_mxn
                if v_mxn > 1.0:
                    wallet_list.append({"TOKEN": coin, "CANTIDAD": cant, "PESOS": f"${v_mxn:,.2f}"})
        
        # PROGRESO A META DE $10K USD
        total_usd = total_mxn / p_usd
        progreso = min(total_usd / 10000.0, 1.0)
        
        st.table(pd.DataFrame(wallet_list))
        st.metric("NET WORTH TOTAL", f"${total_mxn:,.2f} MXN")
        
        st.write(f"**Cazando el objetivo ($10K):** {progreso*100:.2f}%")
        st.progress(progreso)
    else:
        st.info("Esperando conexión con Bitso para desplegar saldos...")

# --- ANÁLISIS TÉCNICO ---
st.divider()
st.subheader("📊 NEON STREAM ANALYSIS")
curr_btc = get_ticker("btc_mxn") or 1260000
df = pd.DataFrame({'Open': [curr_btc]*12, 'High': [curr_btc*1.001]*12, 'Low': [curr_btc*0.999]*12, 'Close': [curr_btc]*12})
df.index = pd.date_range(start=datetime.now(), periods=12, freq='H')
mc = mpf.make_marketcolors(up='#00f2ff', down='#bc13fe', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#1a1a3a', facecolor='#020205', edgecolor='#bc13fe')
buf = BytesIO()
mpf.plot(df, type='candle', style=s, figratio=(16,6), savefig=dict(fname=buf, dpi=100))
st.image(buf, use_container_width=True)
