import streamlit as st
import time, requests, hashlib, hmac, os
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- SHARK TANK AUTHENTICATION ---
# Eliminamos espacios en blanco por si acaso al copiar/pegar
API_KEY = st.secrets.get("BITSO_API_KEY", "").strip()
API_SECRET = st.secrets.get("BITSO_API_SECRET", "").strip()

st.set_page_config(layout="wide", page_title="SHARK TANK | NEURAL CORE")

# --- CYBERPUNK SHARK STYLE ---
st.markdown("""
    <style>
    .stApp { background: #00050a; color: #00f2ff; font-family: 'Trebuchet MS', sans-serif; }
    .stMetric { background: rgba(0, 20, 40, 0.6); border: 2px solid #00f2ff; border-radius: 10px; box-shadow: 0 0 20px #00f2ff; }
    h1, h2, h3 { color: #00f2ff !important; text-shadow: 2px 2px 10px #00f2ff; text-align: center; font-weight: bold; }
    .shark-log { 
        background: #000c1a; border-left: 5px solid #00f2ff; padding: 15px; 
        font-family: 'Consolas', monospace; color: #a0f9ff; height: 300px; overflow-y: scroll;
    }
    div[data-testid="stMetricValue"] { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

class SharkEngine:
    def __init__(self):
        self.base = "https://api.bitso.com"

    def get_balances(self):
        if not API_KEY or not API_SECRET:
            return None, "MISSING_KEYS: Check Streamlit Secrets."
        
        path = "/v3/balances/"
        nonce = str(int(time.time() * 1000))
        message = nonce + "GET" + path
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
        
        headers = {
            'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}',
            'Content-Type': 'application/json'
        }
        
        try:
            r = requests.get(self.base + path, headers=headers, timeout=10)
            res_data = r.json()
            if r.status_code == 200:
                return res_data['payload']['balances'], "SUCCESS"
            else:
                return None, f"BITSO_REJECTED: {res_data.get('error', {}).get('message', 'Unknown Error')}"
        except Exception as e:
            return None, f"CONNECTION_FAILED: {str(e)}"

    def get_price(self, book):
        try:
            r = requests.get(f"{self.base}/v3/ticker/?book={book}").json()
            return float(r['payload']['last'])
        except: return 0.0

bot = SharkEngine()
st.markdown("<h1>🦈 SHARK TANK: QUANTUM TERMINAL v4.0 🦈</h1>", unsafe_allow_html=True)

# --- REAL-TIME MARKET BAR ---
p_btc = bot.get_price("btc_mxn")
p_eth = bot.get_price("eth_mxn")
p_usd = bot.get_price("usd_mxn") or 18.20

c1, c2, c3 = st.columns(3)
c1.metric("BITCOIN / MXN", f"${p_btc:,.2f}")
c2.metric("ETHEREUM / MXN", f"${p_eth:,.2f}")
c3.metric("USD / MXN", f"${p_usd:,.2f}")

st.divider()

# --- PORTFOLIO ANALYSIS ---
raw_balances, status = bot.get_balances()
total_net_worth = 0.0
thoughts = []

if status == "SUCCESS":
    for b in raw_balances:
        amount = float(b['total'])
        if amount > 0.000001:
            coin = b['currency'].lower()
            price = 1.0 if coin == 'mxn' else bot.get_price(f"{coin}_mxn")
            if price == 0: price = bot.get_price(f"{coin}_usd") * p_usd
            
            value = amount * price
            total_net_worth += value
            if value > 0.5: # Only show assets > $0.50 MXN
                thoughts.append(f"HOLDING {coin.upper()}: {amount:.6f} (Value: ${value:,.2f} MXN)")
else:
    thoughts.append(f"ERROR: {status}")

# --- MAIN DASHBOARD ---
col_chart, col_intel = st.columns([2, 1])

with col_chart:
    st.markdown("### 📈 PREDATORY CHART ANALYSIS")
    # Gráfica Shark Blue
    df = pd.DataFrame({'Open': [p_btc*(0.98+i*0.002) for i in range(20)], 'High': [p_btc*1.01 for _ in range(20)],
                       'Low': [p_btc*0.97 for _ in range(20)], 'Close': [p_btc*(0.99+i*0.001) for i in range(20)], 'Volume': [100]*20})
    df.index = pd.date_range(start=datetime.now(), periods=20, freq='H')
    mc = mpf.make_marketcolors(up='#00f2ff', down='#00454d', inherit=True)
    s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#001a2e', facecolor='#00050a', edgecolor='#00f2ff')
    buf = BytesIO(); mpf.plot(df, type='candle', style=s, figratio=(16,9), savefig=dict(fname=buf, dpi=100))
    st.image(buf, use_container_width=True)

with col_intel:
    st.markdown("### 🧠 SHARK INTELLIGENCE")
    log_content = '<div class="shark-log">'
    log_content += f"<p>[{datetime.now().strftime('%H:%M:%S')}] > SYSTEM INITIALIZED.</p>"
    for t in thoughts:
        log_content += f"<p style='color:#00f2ff'>[{datetime.now().strftime('%H:%M:%S')}] > {t}</p>"
    log_content += f"<p style='color:yellow'>[{datetime.now().strftime('%H:%M:%S')}] > STRATEGY: Hunting for entries under $20 MXN.</p>"
    log_content += '</div>'
    st.markdown(log_content, unsafe_allow_html=True)
    st.button("EXECUTE TRADE (SHARK MODE)")

# --- GLOBAL GOAL ---
st.divider()
target_mxn = 10000 * p_usd
progress = min(total_net_worth / target_mxn, 1.0)

st.markdown(f"### 🎯 TARGET $10,000 USD: {progress*100:.4f}%")
st.progress(progress)
st.write(f"💰 REAL BALANCE: **${total_net_worth:,.2f} MXN** | REMAINING: **${(target_mxn - total_net_worth):,.2f} MXN**")
