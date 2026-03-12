import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CONFIGURACIÓN DE SEGURIDAD (SHARK MODE) ---
# Limpieza profunda de llaves para evitar el error 'error'
BITSO_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
BITSO_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

st.set_page_config(layout="wide", page_title="SHARK TANK | PORTFOLIO")

# Estilo TradingView Dark
st.markdown("""
    <style>
    .stApp { background: #0b0e14; color: #d1d4dc; }
    .stMetric { background: #161a25; border: 1px solid #2a2e39; border-radius: 8px; }
    h1, h2, h3 { color: #2962ff !important; font-family: 'Trebuchet MS', sans-serif; }
    .status-box { padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #2a2e39; }
    </style>
    """, unsafe_allow_html=True)

class SharkBot:
    def __init__(self):
        self.url = "https://api.bitso.com"

    def get_price(self, book):
        try:
            r = requests.get(f"{self.url}/v3/ticker/?book={book}", timeout=5).json()
            return float(r['payload']['last'])
        except: return 0.0

    def fetch_balances(self):
        if not BITSO_KEY or not BITSO_SECRET:
            return None, "Faltan llaves en Streamlit Secrets"
        
        nonce = str(int(time.time() * 1000))
        path = "/v3/balances/"
        # Firma ultra limpia
        message = nonce + "GET" + path
        signature = hmac.new(BITSO_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
        
        headers = {
            'Authorization': f'Bitso {BITSO_KEY}:{nonce}:{signature}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(self.url + path, headers=headers, timeout=10)
            res_data = response.json()
            if response.status_code == 200:
                return res_data['payload']['balances'], "SUCCESS"
            else:
                return None, res_data.get('error', {}).get('message', 'Error desconocido')
        except Exception as e:
            return None, f"Error de Red: {str(e)}"

bot = SharkBot()
st.title("🦈 SHARK TANK: MY INVESTMENTS")

# --- MONITOR DE PRECIOS ---
p_usd = bot.get_price("usd_mxn") or 18.20
assets = ["btc_mxn", "eth_mxn", "usd_mxn"]
t_cols = st.columns(3)
for i, a in enumerate(assets):
    t_cols[i].metric(a.split('_')[0].upper(), f"${bot.get_price(a):,.2f} MXN")

st.divider()

# --- BILLETERA Y DATOS ---
bal, status = bot.fetch_balances()

if status == "SUCCESS":
    st.subheader("📂 Real-Time Wallet (Crypto & USD)")
    rows = []
    total_mxn = 0.0
    for b in bal:
        qty = float(b['total'])
        if qty > 0.00000001:
            coin = b['currency'].upper()
            price = 1.0 if coin == 'MXN' else bot.get_price(f"{coin.lower()}_mxn")
            if price == 0: price = bot.get_price(f"{coin.lower()}_usd") * p_usd
            
            val_mxn = qty * price
            total_mxn += val_mxn
            rows.append({
                "MONEDA": coin,
                "CANTIDAD": f"{qty:.8f}",
                "VALOR MXN": f"${val_mxn:,.2f}",
                "VALOR USD": f"${(val_mxn/p_usd):,.2f}"
            })
    
    if rows:
        st.table(pd.DataFrame(rows))
        
        # Resumen final
        c1, c2 = st.columns(2)
        c1.metric("TOTAL PORTAFOLIO (MXN)", f"${total_mxn:,.2f}")
        
        progreso = min((total_mxn/p_usd) / 10000, 1.0)
        st.write(f"**Progreso hacia $10,000 USD: {progreso*100:.4f}%**")
        st.progress(progreso)
    else:
        st.info("No tienes saldos activos en Bitso.")
else:
    st.error(f"⚠️ ERROR DE AUTENTICACIÓN: {status}")
    st.markdown("""
    **¿Cómo arreglarlo?**
    1. Asegúrate de que en Bitso el permiso sea **"Consultar Saldos"**.
    2. En Streamlit Secrets, revisa que no haya comillas extras o espacios.
    3. Si el error persiste, intenta generar una API KEY nueva **sin límite de IP**.
    """)

# --- GRÁFICA ---
st.divider()
st.subheader("📈 Análisis de Tendencia (BTC)")
p_btc = bot.get_price("btc_mxn") or 1230000
df = pd.DataFrame({'Open': [p_btc]*20, 'High': [p_btc*1.002]*20, 'Low': [p_btc*0.998]*20, 'Close': [p_btc]*20, 'Volume': [100]*20})
df.index = pd.date_range(start=datetime.now(), periods=20, freq='15min')
mc = mpf.make_marketcolors(up='#26a69a', down='#ef5350', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#2a2e39', facecolor='#0b0e14', edgecolor='#2a2e39')
buf = BytesIO(); mpf.plot(df, type='candle', style=s, figratio=(16,6), savefig=dict(fname=buf, dpi=100))
st.image(buf, use_container_width=True)
