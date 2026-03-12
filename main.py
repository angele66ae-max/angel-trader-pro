import streamlit as st
import time, requests, hashlib, hmac, os
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- SHARK AUTH (REPARADO) ---
API_KEY = st.secrets.get("BITSO_API_KEY", "").strip()
API_SECRET = st.secrets.get("BITSO_API_SECRET", "").strip()

st.set_page_config(layout="wide", page_title="SHARK TANK | PRO TRADER")

# --- TRADINGVIEW DARK STYLE ---
st.markdown("""
    <style>
    .stApp { background: #131722; color: #d1d4dc; font-family: 'Trebuchet MS', sans-serif; }
    .stMetric { background: #1e222d; border: 1px solid #363a45; border-radius: 5px; padding: 10px; }
    h1 { color: #2962ff !important; text-shadow: 0 0 10px #2962ff; }
    .shark-log { 
        background: #1e222d; border: 1px solid #363a45; padding: 15px; 
        font-family: 'Consolas', monospace; color: #00ff88; height: 350px; overflow-y: scroll;
    }
    div[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 24px !important; }
    </style>
    """, unsafe_allow_html=True)

class SharkEngine:
    def __init__(self):
        self.base = "https://api.bitso.com"
        self.assets = ["btc_mxn", "eth_mxn", "usd_mxn", "nvda_usd", "aapl_usd"]

    def get_balances(self):
        if not API_KEY: return None, "MISSING_KEYS"
        path = "/v3/balances/"
        nonce = str(int(time.time() * 1000))
        # CORRECCIÓN DE LA LÍNEA 38:
        message = nonce + "GET" + path
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
        
        try:
            r = requests.get(self.base + path, headers=headers, timeout=10)
            return (r.json()['payload']['balances'], "SUCCESS") if r.status_code == 200 else (None, "AUTH_ERROR")
        except: return None, "CONNECTION_FAILED"

    def get_price(self, book):
        try:
            r = requests.get(f"{self.base}/v3/ticker/?book={book}").json()
            return float(r['payload']['last'])
        except: return 0.0

bot = SharkEngine()
st.title("🦈 SHARK TANK: PRO TRADING TERMINAL")

# --- TOP TICKER BAR ---
prices = {}
ticker_cols = st.columns(len(bot.assets))
for i, asset in enumerate(bot.assets):
    p = bot.get_price(asset)
    prices[asset] = p
    ticker_cols[i].metric(asset.split('_')[0].upper(), f"${p:,.2f}")

st.divider()

# --- MAIN INTERFACE ---
col_chart, col_intel = st.columns([3, 1])

with col_chart:
    selected_asset = st.selectbox("📊 SELECT MARKET", bot.assets, index=0)
    current_p = prices[selected_asset]
    
    # Simulación de velas estilo TradingView
    df = pd.DataFrame({
        'Open': [current_p * (0.998 + (i*0.0001)) for i in range(50)],
        'High': [current_p * 1.002 for _ in range(50)],
        'Low': [current_p * 0.995 for _ in range(50)],
        'Close': [current_p * (0.999 + (i*0.0001)) for i in range(50)],
        'Volume': [1000 for _ in range(50)]
    })
    df.index = pd.date_range(start=datetime.now(), periods=50, freq='15min')
    
    # Velas Verdes y Rojas clásicas
    mc = mpf.make_marketcolors(up='#26a69a', down='#ef5350', inherit=True)
    s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#363a45', facecolor='#131722', edgecolor='#363a45')
    
    buf = BytesIO()
    mpf.plot(df, type='candle', style=s, figratio=(18,9), savefig=dict(fname=buf, dpi=150))
    st.image(buf, use_container_width=True)

with col_intel:
    st.markdown("### 🧠 SHARK INTEL")
    raw_bal, status = bot.get_balances()
    total_mxn = 0.0
    
    log_content = '<div class="shark-log">'
    if status == "SUCCESS":
        for b in raw_bal:
            qty = float(b['total'])
            if qty > 0.000001:
                coin = b['currency'].lower()
                p_val = 1.0 if coin == 'mxn' else bot.get_price(f"{coin}_mxn")
                if p_val == 0: p_val = bot.get_price(f"{coin}_usd") * prices.get('usd_mxn', 18.2)
                
                value = qty * p_val
                total_mxn += value
                if value > 0.1:
                    log_content += f"<p>💰 {coin.upper()}: {qty:.4f}<br><small>(${value:,.2f} MXN)</small></p>"
    else:
        log_content += f"<p style='color:#ef5350'>⚠️ STATUS: {status}</p>"
    
    log_content += '</div>'
    st.markdown(log_content, unsafe_allow_html=True)
    st.button("⚡ FORCE SCAN")

# --- GLOBAL PROGRESS ---
st.divider()
target_mxn = 10000 * (prices.get('usd_mxn') or 18.2)
progress_pct = min(total_mxn / target_mxn, 1.0)

f1, f2 = st.columns(2)
f1.metric("PORTFOLIO VALUE", f"${total_mxn:,.2f} MXN")
f2.metric("PROGRESS TO $10K USD", f"{progress_pct*100:.4f}%")
st.progress(progress_pct)
