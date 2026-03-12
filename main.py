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

# --- TRADINGVIEW STYLE ---
st.markdown("""
    <style>
    .stApp { background: #131722; color: #d1d4dc; }
    .stMetric { background: #1e222d; border: 1px solid #363a45; border-radius: 4px; }
    .shark-log { background: #1e222d; border: 1px solid #363a45; padding: 10px; color: #00ff88; height: 300px; overflow-y: auto; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

class SharkEngine:
    def __init__(self):
        self.base = "https://api.bitso.com"

    def get_balances(self):
        path = "/v3/balances/"
        nonce = str(int(time.time() * 1000))
        # Generación de firma ultra-limpia
        msg = nonce + "GET" + path
        signature = hmac.new(API_SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest()
        auth_header = f"Bitso {API_KEY}:{nonce}:{signature}"
        
        try:
            r = requests.get(self.base + path, headers={'Authorization': auth_header}, timeout=10)
            data = r.json()
            if r.status_code == 200:
                return data['payload']['balances'], "SUCCESS"
            else:
                return None, f"BITSO_SAYS: {data['error']['message']}"
        except Exception as e:
            return None, f"SYSTEM_ERROR: {str(e)}"

    def get_price(self, book):
        try:
            r = requests.get(f"{self.base}/v3/ticker/?book={book}").json()
            return float(r['payload']['last'])
        except: return 0.0

bot = SharkEngine()
st.title("🦈 SHARK TANK: PRO TRADING TERMINAL")

# --- PRICES ---
p_usd = bot.get_price("usd_mxn") or 18.20
assets = ["btc_mxn", "eth_mxn", "usd_mxn", "nvda_usd", "aapl_usd"]
prices = {a: bot.get_price(a) for a in assets}

cols = st.columns(len(assets))
for i, a in enumerate(assets):
    cols[i].metric(a.split('_')[0].upper(), f"${prices[a]:,.2f}")

st.divider()

col_left, col_right = st.columns([3, 1])

with col_left:
    selected = st.selectbox("CHOOSE MARKET", assets)
    curr = prices[selected]
    # Simulación de velas profesional
    df = pd.DataFrame({'Open': [curr*(1+i*0.0001) for i in range(50)], 'High': [curr*1.002 for _ in range(50)],
                       'Low': [curr*0.998 for _ in range(50)], 'Close': [curr*(1.001+i*0.0001) for i in range(50)], 'Volume': [100]*50})
    df.index = pd.date_range(start=datetime.now(), periods=50, freq='15min')
    mc = mpf.make_marketcolors(up='#26a69a', down='#ef5350', inherit=True)
    s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#363a45', facecolor='#131722', edgecolor='#363a45')
    buf = BytesIO(); mpf.plot(df, type='candle', style=s, figratio=(18,9), savefig=dict(fname=buf, dpi=120))
    st.image(buf, use_container_width=True)

with col_right:
    st.markdown("### 🧠 SHARK INTEL")
    bal, status = bot.get_balances()
    total_mxn = 0.0
    log = '<div class="shark-log">'
    
    if status == "SUCCESS":
        for b in bal:
            q = float(b['total'])
            if q > 0:
                coin = b['currency'].lower()
                p = 1.0 if coin == 'mxn' else bot.get_price(f"{coin}_mxn")
                if p == 0: p = bot.get_price(f"{coin}_usd") * p_usd
                val = q * p
                total_mxn += val
                if val > 0.1:
                    log += f"<p>✅ {coin.upper()}: {q:.5f}<br><small>${val:,.2f} MXN</small></p>"
    else:
        log += f"<p style='color:#ef5350'>⚠️ {status}</p>"
        log += "<p><small>Check API Permissions: 'Saldos' must be ON.</small></p>"
    
    log += '</div>'
    st.markdown(log, unsafe_allow_html=True)

# --- FOOTER ---
st.divider()
target = 10000 * p_usd
prog = min(total_mxn / target, 1.0)
c_f1, c_f2 = st.columns(2)
c_f1.metric("REAL PORTFOLIO", f"${total_mxn:,.2f} MXN")
c_f2.metric("GOAL $10K USD", f"{prog*100:.4f}%")
st.progress(prog)
