import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="SHARK NEON v8.8")

# --- CREDENCIALES (LIMPIEZA TOTAL) ---
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

# --- ESTILO SHARK NEÓN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    .stApp { background-color: #020205; color: #bc13fe; font-family: 'JetBrains Mono', monospace; }
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #00d4ff !important; text-shadow: 0 0 10px #bc13fe; }
    .status-box { background: rgba(20, 0, 40, 0.8); border: 2px solid #00d4ff; padding: 15px; border-radius: 10px; box-shadow: 0 0 15px #bc13fe; }
    .stMetric { background: rgba(0, 0, 0, 0.5); border: 1px solid #bc13fe; border-radius: 5px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

def bitso_request(path):
    """Protocolo de Conexión Blindada"""
    nonce = str(int(time.time() * 1000))
    # El mensaje de firma NO debe tener la diagonal final si el path no la tiene
    message = nonce + "GET" + path
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    
    headers = {
        'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}',
        'Content-Type': 'application/json'
    }
    # Usamos el host de API secundario que suele evitar el error de 'static resource'
    return requests.get(f"https://api.bitso.com{path}", headers=headers, timeout=15)

def get_data():
    if not API_KEY or not API_SECRET: return None, "Faltan Credenciales"
    
    # Probamos la ruta estándar de balances
    path = "/v3/account_status" # Cambiamos a status primero para validar conexión
    try:
        r = bitso_request("/v3/balances")
        if r.status_code == 200: 
            return r.json()['payload']['balances'], "OK"
        else:
            return None, f"Bitso dice: {r.status_code}"
    except Exception as e: 
        return None, f"Error de Red: {str(e)}"

def get_ticker(book):
    try:
        # Los tickers son públicos, no necesitan firma
        r = requests.get(f"https://api.bitso.com/v3/ticker/?book={book}").json()
        return float(r['payload']['last'])
    except: return 0.0

# --- INTERFAZ ---
st.title("🦈 SHARK SYSTEM: NEON CORE v8.8")

col_main, col_side = st.columns([2, 1])

with col_side:
    st.subheader("📡 SISTEMA")
    balances, status = get_data()
    st.markdown(f"""
    <div class="status-box">
        <b>ESTADO:</b> {"🟢 CONECTADO" if status == "OK" else "🔴 RE-SINCRONIZANDO"}<br>
        <b>MOTOR:</b> SHARK-IA v8.8<br>
        <b>LLAVE:</b> {API_KEY[:5]}***
    </div>
    """, unsafe_allow_html=True)
    
    if status != "OK":
        st.error(f"Detalle: {status}")
        st.info("💡 **TIP MAESTRO:** Si esto falla, ve a Bitso y crea una llave nueva que se llame 'SharkV8'. Dale permiso de 'Ver saldos' y NO le pongas ninguna IP.")

with col_main:
    p_usd = get_ticker("usd_mxn") or 18.00
    m1, m2, m3 = st.columns(3)
    m1.metric("₿ BTC", f"${get_ticker('btc_mxn'):,.0f} MXN")
    m2.metric("Ξ ETH", f"${get_ticker('eth_mxn'):,.0f} MXN")
    m3.metric("🌐 USD/MXN", f"${p_usd:,.2f}")

    if status == "OK":
        st.divider()
        st.subheader("💰 BILLETERA NEÓN")
        df_data = []
        total_mxn = 0.0
        for b in balances:
            cant = float(b['total'])
            if cant > 0.00000001:
                coin = b['currency'].upper()
                price = 1.0 if coin == "MXN" else get_ticker(f"{coin.lower()}_mxn")
                v_mxn = cant * price
                total_mxn += v_mxn
                df_data.append({"TOKEN": coin, "CANTIDAD": cant, "VALOR MXN": f"${v_mxn:,.2f}"})
        
        if df_data:
            st.table(pd.DataFrame(df_data))
            st.metric("TOTAL ESTIMADO", f"${total_mxn:,.2f} MXN")
            
            # Cálculo para tu meta de la SUV
            meta = 1700000
            falta = max(0, meta - total_mxn)
            progreso = min(total_mxn / meta, 1.0)
            st.write(f"**Progreso para la camioneta ($1.7M):** {progreso*100:.2f}%")
            st.progress(progreso)

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
