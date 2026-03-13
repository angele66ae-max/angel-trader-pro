import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CONFIGURACIÓN DE ESTILO ---
st.set_page_config(layout="wide", page_title="SHARK NEON v8.1")

st.markdown("""
    <style>
    /* Efecto Shark Attack (Sacudida y Brillo Rojo) */
    @keyframes shark-bite {
        0% { transform: scale(1); background-color: #020205; }
        10% { transform: scale(1.03) rotate(1deg); background-color: #ff000033; }
        50% { transform: scale(0.97) rotate(-1deg); background-color: #ff000055; }
        100% { transform: scale(1); background-color: #020205; }
    }
    .shark-active { animation: shark-bite 0.6s ease-in-out; }
    .stApp { background-color: #020205; color: #bc13fe; font-family: 'JetBrains Mono', monospace; }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #bc13fe, #00d4ff);
        box-shadow: 0 0 15px #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CREDENCIALES ---
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

def get_bitso_balances():
    if not API_KEY or not API_SECRET: return None, "Faltan Credenciales"
    
    # RUTA CRÍTICA: Se eliminó la diagonal final que causa el 404
    host = "https://api.bitso.com"
    path = "/v3/balances"
    
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + path
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    
    try:
        r = requests.get(host + path, headers=headers, timeout=10)
        if r.status_code == 200: return r.json()['payload']['balances'], "OK"
        return None, f"Error {r.status_code}: {r.text}"
    except Exception as e: return None, str(e)

def get_price(book):
    try:
        r = requests.get(f"https://api.bitso.com/v3/ticker/?book={book}").json()
        return float(r['payload']['last'])
    except: return 0.0

# --- LÓGICA DE INTERFAZ ---
balances, status = get_bitso_balances()

# Si los datos cargan, activamos el efecto de mordida
if status == "OK":
    st.markdown('<div class="shark-active"></div>', unsafe_allow_html=True)

st.title("🦈 SHARK SYSTEM: NEON CORE v8.1")

if status == "OK":
    total_mxn = 0.0
    wallet_data = []
    usd_mxn = get_price("usd_mxn") or 18.00
    
    for b in balances:
        amount = float(b['total'])
        if amount > 0:
            coin = b['currency'].upper()
            price = 1.0 if coin == "MXN" else get_price(f"{coin.lower()}_mxn")
            val_mxn = amount * price
            total_mxn += val_mxn
            if val_mxn > 1.0:
                wallet_data.append({"TOKEN": coin, "CANTIDAD": amount, "VALOR MXN": f"${val_mxn:,.2f}"})
    
    # CÁLCULO DE META
    total_usd = total_mxn / usd_mxn
    progreso = min(total_usd / 10000.0, 1.0)
    
    c1, c2 = st.columns(2)
    c1.metric("BILLETERA (MXN)", f"${total_mxn:,.2f}")
    c2.metric("PROGRESO USD", f"${total_usd:,.2f} / $10,000")
    
    st.write(f"**Estatus del Depredador:** {progreso*100:.2f}%")
    st.progress(progreso)
    st.dataframe(pd.DataFrame(wallet_data), use_container_width=True)
else:
    # Guía de reparación basada en tus logs
    st.error(f"⚠️ {status}")
    st.warning("⚠️ REVISA TUS PERMISOS EN BITSO:")
    st.info("1. Entra a Bitso > Perfil > API.\n2. La llave debe tener permiso de 'Consultar Saldos' (Account Balances).\n3. ¡IMPORTANTE!: No pongas ninguna dirección IP en la lista blanca (déjala vacía).")

# --- GRÁFICA ---
st.divider()
st.subheader("📊 MARKET STREAM ANALYSIS")
curr_btc = get_price("btc_mxn") or 1200000
df = pd.DataFrame({'Open': [curr_btc]*10, 'High': [curr_btc*1.01]*10, 'Low': [curr_btc*0.99]*10, 'Close': [curr_btc]*10})
df.index = pd.date_range(start=datetime.now(), periods=10, freq='H')
mc = mpf.make_marketcolors(up='#00f2ff', down='#bc13fe', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#0d1117', facecolor='#020205', edgecolor='#bc13fe')
buf = BytesIO()
mpf.plot(df, type='candle', style=s, figratio=(16,6), savefig=dict(fname=buf, dpi=100))
st.image(buf, use_container_width=True)
