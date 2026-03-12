import streamlit as st
import time, requests, hashlib, hmac, os
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- SHARK AUTH ---
API_KEY = st.secrets.get("BITSO_API_KEY", "").strip()
API_SECRET = st.secrets.get("BITSO_API_SECRET", "").strip()

st.set_page_config(layout="wide", page_title="SHARK TANK | PRO")

# --- TRADINGVIEW DARK STYLE ---
st.markdown("""
    <style>
    .stApp { background: #131722; color: #d1d4dc; }
    .stMetric { background: #1e222d; border: 1px solid #363a45; border-radius: 4px; padding: 10px; }
    .shark-log { background: #1e222d; border: 1px solid #363a45; padding: 15px; color: #00ff88; height: 300px; overflow-y: auto; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

class SharkEngine:
    def __init__(self):
        self.base = "https://api.bitso.com"

    def get_balances(self):
        if not API_KEY or not API_SECRET:
            return None, "ERROR: Keys missing in Secrets"
        
        path = "/v3/balances/"
        nonce = str(int(time.time() * 1000))
        message = nonce + "GET" + path
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
        
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
        
        try:
            r = requests.get(self.base + path, headers=headers, timeout=10)
            data = r.json()
            if r.status_code == 200:
                return data['payload']['balances'], "OK"
            else:
                return None, f"Bitso Error: {data.get('error', {}).get('message', 'Check Permissions')}"
        except Exception as e:
            return None, f"Connection Error: {str(e)}"

    def get_price(self, book):
        try:
            r = requests.get(f"{self.base}/v3/ticker/?book={book}").json()
            return float(r['payload']['last'])
        except: return 0.0

bot = SharkEngine()
st.title("🦈 SHARK TANK: PRO TERMINAL")

# --- TICKERS ---
assets = ["btc_mxn", "eth_mxn", "usd_mxn"]
prices = {a: bot.get_price(a) for a in assets}

c1, c2, c3 = st.columns(3)
c1.metric("BITCOIN", f"${prices['btc_mxn']:,.2f}")
c2.metric("ETHEREUM", f"${prices['eth_mxn']:,.2f}")
c3.metric("DÓLAR", f"${prices['usd_mxn']:,.2f}")

st.divider()

col_left, col_right = st.columns([3, 1])

with col_left:
    st.subheader("📈 MARKET CHART (15m)")
    # Gráfica técnica
    curr = prices['btc_mxn']
    df = pd.DataFrame({
        'Open': [curr * (0.999 + i*0.0001) for i in range(40)],
        'High': [curr * 1.002 for _ in range(40)],
        'Low': [curr * 0.997 for _ in range(40)],
        'Close': [curr * (1.001 + i*0.0001) for i in range(40)],
        'Volume': [100]*40
    })
    df.index = pd.date_range(start=datetime.now(), periods=40, freq='15min')
    mc = mpf.make_marketcolors(up='#26a69a', down='#ef5350', inherit=True)
    s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#363a45', facecolor='#131722', edgecolor='#363a45')
    buf = BytesIO(); mpf.plot(df, type='candle', style=s, figratio=(18,9), savefig=dict(fname=buf, dpi=120))
    st.image(buf, use_container_width=True)

with col_right:
    st.subheader("🧠 SHARK INTEL")
    balances, status = bot.get_balances()
    total_val = 0.0
    
    log = '<div class="shark-log">'
    if status == "OK":
        for b in balances:
            q = float(b['total'])
            if q > 0:
                coin = b['currency'].lower()
                p = 1.0 if coin == 'mxn' else bot.get_price(f"{coin}_mxn")
                if p == 0: p = bot.get_price(f"{coin}_usd") * prices['usd_mxn']
                val = q * p
                total_val += val
                if val > 1.0:
                    log += f"<p style='margin:0;'>✅ {coin.upper()}: {q:.4f}</p>"
                    log += f"<p style='color:#5d606b; font-size:12px;'>Value: ${val:,.2f} MXN</p><hr style='border:0.1px solid #363a45'>"
    else:
        log += f"<p style='color:#ef5350;'>{status}</p>"
        log += "<p style='font-size:12px;'>Go to Bitso > Profile > API and enable 'Consultar Saldos'.</p>"
    
    log += '</div>'
    st.markdown(log, unsafe_allow_html=True)
    st.metric("TOTAL PORTFOLIO", f"${total_val:,.2f} MXN")

# --- PROGRESS ---
st.divider()
target_mxn = 10000 * (prices['usd_mxn'] or 18.2)
prog = min(total_val / target_mxn, 1.0)
st.write(f"**GOAL PROGRESS TO $10K USD: {prog*100:.4f}%**")
st.progress(prog)
