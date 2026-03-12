import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- SHARK AUTH ---
API_KEY = st.secrets.get("BITSO_API_KEY", "").strip()
API_SECRET = st.secrets.get("BITSO_API_SECRET", "").strip()

st.set_page_config(layout="wide", page_title="SHARK TANK | WALLET")

# --- DARK STYLE ---
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #e0e0e0; }
    .wallet-box { background: #1c2128; border: 1px solid #30363d; border-radius: 8px; padding: 20px; }
    h2 { color: #2962ff !important; }
    </style>
    """, unsafe_allow_html=True)

class SharkEngine:
    def __init__(self):
        self.base = "https://api.bitso.com"

    def get_price(self, book):
        try:
            r = requests.get(f"{self.base}/v3/ticker/?book={book}").json()
            return float(r['payload']['last'])
        except: return 0.0

    def get_balances(self):
        if not API_KEY: return None, "KEYS_MISSING"
        path = "/v3/balances/"
        nonce = str(int(time.time() * 1000))
        signature = hmac.new(API_SECRET.encode(), (nonce + "GET" + path).encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
        try:
            r = requests.get(self.base + path, headers=headers, timeout=10)
            return (r.json()['payload']['balances'], "OK") if r.status_code == 200 else (None, "AUTH_ERROR")
        except: return None, "CONN_ERROR"

bot = SharkEngine()
p_usd_mxn = bot.get_price("usd_mxn") or 18.20

st.title("🦈 SHARK TANK: MY ASSETS")

# --- SECCIÓN 1: MI BILLETERA DETALLADA ---
st.header("📂 My Crypto Wallet")
bal, status = bot.get_balances()
total_mxn = 0.0

if status == "OK":
    wallet_list = []
    for b in bal:
        qty = float(b['total'])
        if qty > 0.00000001:
            coin = b['currency'].upper()
            # Obtener precio para conversión
            price_mxn = 1.0 if coin == 'MXN' else bot.get_price(f"{coin.lower()}_mxn")
            if price_mxn == 0: price_mxn = bot.get_price(f"{coin.lower()}_usd") * p_usd_mxn
            
            value_mxn = qty * price_mxn
            value_usd = value_mxn / p_usd_mxn
            total_mxn += value_mxn
            
            wallet_list.append({
                "ASSET": coin,
                "BALANCE": f"{qty:.8f}",
                "VALUE (MXN)": f"${value_mxn:,.2f}",
                "VALUE (USD)": f"${value_usd:,.2f}"
            })
    
    if wallet_list:
        st.table(pd.DataFrame(wallet_list))
    else:
        st.info("No active balances found.")
else:
    st.error(f"Status: {status}. Check your API Keys and permissions.")

st.divider()

# --- SECCIÓN 2: GRÁFICA Y RESUMEN ---
col_chart, col_summary = st.columns([2, 1])

with col_chart:
    st.subheader("📈 Market View (BTC)")
    curr = bot.get_price("btc_mxn")
    df = pd.DataFrame({'Open': [curr]*20, 'High': [curr*1.01]*20, 'Low': [curr*0.99]*20, 'Close': [curr]*20, 'Volume': [100]*20})
    df.index = pd.date_range(start=datetime.now(), periods=20, freq='H')
    mc = mpf.make_marketcolors(up='#26a69a', down='#ef5350', inherit=True)
    s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#363a45', facecolor='#131722', edgecolor='#363a45')
    buf = BytesIO(); mpf.plot(df, type='candle', style=s, figratio=(16,7), savefig=dict(fname=buf, dpi=100))
    st.image(buf, use_container_width=True)

with col_summary:
    st.subheader("🏆 Total Wealth")
    st.metric("TOTAL MXN", f"${total_mxn:,.2f}")
    st.metric("TOTAL USD", f"${(total_mxn/p_usd_mxn):,.2f}")
    
    # Progress to $10k USD
    target_mxn = 10000 * p_usd_mxn
    prog = min(total_mxn / target_mxn, 1.0)
    st.write(f"Goal Progress: {prog*100:.4f}%")
    st.progress(prog)
