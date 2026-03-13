import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="SHARK NEON v8.2")

# --- CREDENCIALES ---
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

# --- ESTILO SHARK ---
st.markdown("""
    <style>
    @keyframes shark-bite {
        0% { transform: scale(1); background-color: #020205; }
        10% { transform: scale(1.02); background-color: #ff000033; }
        100% { transform: scale(1); background-color: #020205; }
    }
    .shark-active { animation: shark-bite 0.5s ease-out; }
    .stApp { background-color: #020205; color: #bc13fe; font-family: 'JetBrains Mono', monospace; }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #bc13fe, #00d4ff);
        box-shadow: 0 0 15px #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

def get_bitso_data():
    if not API_KEY or not API_SECRET: return None, "Faltan Credenciales"
    
    # CORRECCIÓN DE RUTA: Bitso v3 requiere el path exacto sin puntos ni barras extra
    host = "https://api.bitso.com"
    path = "/v3/balances" # Esta es la ruta que tus permisos 'Ver saldos' necesitan
    
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + path
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    
    try:
        r = requests.get(host + path, headers=headers, timeout=10)
        if r.status_code == 200: 
            return r.json()['payload']['balances'], "OK"
        # Captura el error detallado que vimos en tu imagen
        return None, f"Error {r.status_code}: {r.json().get('error', {}).get('message', 'Not Found')}"
    except Exception as e: 
        return None, str(e)

def get_ticker(book):
    try:
        r = requests.get(f"https://api.bitso.com/v3/ticker/?book={book}").json()
        return float(r['payload']['last'])
    except: return 0.0

# --- LÓGICA PRINCIPAL ---
balances, status = get_bitso_data()

if status == "OK":
    st.markdown('<div class="shark-active"></div>', unsafe_allow_html=True)

st.title("🦈 SHARK SYSTEM: NEON CORE v8.2")

if status == "OK":
    total_mxn = 0.0
    p_usd = get_ticker("usd_mxn") or 17.82
    
    # Procesar saldos de la API 'casa tiburones'
    wallet_list = []
    for b in balances:
        cant = float(b['total'])
        if cant > 0:
            coin = b['currency'].upper()
            price = 1.0 if coin == "MXN" else get_ticker(f"{coin.lower()}_mxn")
            val = cant * price
            total_mxn += val
            if val > 1.0:
                wallet_list.append({"TOKEN": coin, "CANTIDAD": cant, "VALOR MXN": f"${val:,.2f}"})
    
    # META $10,000 USD
    total_usd = total_mxn / p_usd
    progreso = min(total_usd / 10000.0, 1.0)
    
    c1, c2 = st.columns(2)
    c1.metric("BILLETERA (MXN)", f"${total_mxn:,.2f}")
    c2.metric("AVANCE A META (USD)", f"${total_usd:,.2f} / $10,000")
    
    st.write(f"**Progreso del Tiburón:** {progreso*100:.2f}%")
    st.progress(progreso)
    st.dataframe(pd.DataFrame(wallet_list), use_container_width=True)
else:
    # Mostrar el error detallado para debug
    st.error(f"⚠️ FALLO DE ENLACE: {status}")
    st.info("Tip: Asegúrate de que el API SECRET en Streamlit coincida con el de 'casa tiburones'.")

# --- GRÁFICA ---
st.divider()
st.subheader("📊 MARKET ANALYSIS")
curr_btc = get_ticker("btc_mxn") or 1250000
df = pd.DataFrame({'Open': [curr_btc]*10, 'High': [curr_btc*1.01]*10, 'Low': [curr_btc*0.99]*10, 'Close': [curr_btc]*10})
df.index = pd.date_range(start=datetime.now(), periods=10, freq='H')
mc = mpf.make_marketcolors(up='#00f2ff', down='#bc13fe', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#0d1117', facecolor='#020205', edgecolor='#bc13fe')
buf = BytesIO()
mpf.plot(df, type='candle', style=s, figratio=(16,6), savefig=dict(fname=buf, dpi=100))
st.image(buf, use_container_width=True)
