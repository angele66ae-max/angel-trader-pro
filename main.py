import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CREDENCIALES ---
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

st.set_page_config(layout="wide", page_title="SHARK TERMINAL v6.4")

# --- ESTILO CYBERPUNK ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #05070a; color: #00ff41; font-family: 'JetBrains Mono', monospace; }
    div[data-testid="stMetricValue"] { color: #00ff41 !important; text-shadow: 0 0 10px #00ff41; }
    .stTable { background: rgba(0, 20, 40, 0.8); border: 1px solid #00d4ff; color: #00ff41; }
    h1, h2 { color: #00d4ff !important; text-transform: uppercase; letter-spacing: 2px; border-left: 4px solid #00d4ff; padding-left: 10px; }
    </style>
    """, unsafe_allow_html=True)

def get_data():
    if not API_KEY or not API_SECRET: return None, "Faltan llaves en Secrets"
    path = "/v3/balances/"
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + path
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    try:
        r = requests.get(f"https://api.bitso.com{path}", headers=headers, timeout=10)
        if r.status_code == 200: return r.json()['payload']['balances'], "OK"
        return None, f"Error {r.status_code}: {r.json().get('error', {}).get('message', 'Auth Fail')}"
    except Exception as e: return None, str(e)

def get_ticker(book):
    try:
        r = requests.get(f"https://api.bitso.com/v3/ticker/?book={book}").json()
        return float(r['payload']['last'])
    except: return 0.0

st.title("🦈 SHARK SYSTEM v6.4")
p_usd = get_ticker("usd_mxn") or 17.80

# --- MERCADO ---
c1, c2, c3 = st.columns(3)
c1.metric("₿ BTC", f"${get_ticker('btc_mxn'):,.0f} MXN")
c2.metric("Ξ ETH", f"${get_ticker('eth_mxn'):,.0f} MXN")
c3.metric("💵 USD/MXN", f"${p_usd:,.2f}")

st.divider()

# --- MI BILLETERA (TU NUEVO APARTADO) ---
st.header("💰 MI BILLETERA CRYPTO")
balances, status = get_data()
total_mxn = 0.0

if status == "OK":
    wallet_list = []
    for b in balances:
        cant = float(b['total'])
        if cant > 0.00000001:
            coin = b['currency'].upper()
            price = 1.0 if coin == "MXN" else get_ticker(f"{coin.lower()}_mxn")
            if price == 0: price = get_ticker(f"{coin.lower()}_usd") * p_usd
            
            val_m = cant * price
            total_mxn += val_m
            
            if val_m > 0.5: # Solo mostrar si tienes más de 50 centavos
                wallet_list.append({
                    "MONEDA": coin,
                    "CANTIDAD": f"{cant:.8f}",
                    "VALOR MXN": f"${val_m:,.2f}",
                    "VALOR USD": f"${(val_m/p_usd):,.2f}"
                })
    
    if wallet_list:
        st.table(pd.DataFrame(wallet_list))
        st.subheader(f"VALOR TOTAL DEL PORTAFOLIO: ${total_mxn:,.2f} MXN")
        
        prog = min((total_mxn/p_usd)/10000, 1.0)
        st.write(f"**META $10K USD: {prog*100:.4f}%**")
        st.progress(prog)
    else:
        st.info("Conexión exitosa, pero no se detectaron fondos.")
else:
    st.error(f"FALLO DE AUTENTICACIÓN: {status}")

# --- GRÁFICA CORREGIDA ---
st.divider()
st.subheader("📉 DATA_STREAM (BTC)")
curr_btc = get_ticker("btc_mxn") or 1235000
df = pd.DataFrame({'Open': [curr_btc]*10, 'High': [curr_btc*1.002]*10, 'Low': [curr_btc*0.998]*10, 'Close': [curr_btc]*10})
df.index = pd.date_range(start=datetime.now(), periods=10, freq='H')

mc = mpf.make_marketcolors(up='#00ff41', down='#ff003c', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#161a25', facecolor='#05070a', edgecolor='#00d4ff')

buf = BytesIO()
mpf.plot(df, type='candle', style=s, figratio=(16,7), savefig=dict(fname=buf, dpi=100))
st.image(buf, use_container_width=True)
