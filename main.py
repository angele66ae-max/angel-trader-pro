import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CREDENCIALES (CORREGIDAS) ---
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

st.set_page_config(layout="wide", page_title="TERMINAL SHARK v6.1")

# --- ESTILO "CYBER_HACKER" ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp { 
        background-color: #05070a; 
        background-image: radial-gradient(#0a192f 0.5px, transparent 0.5px);
        background-size: 20px 20px;
        font-family: 'JetBrains Mono', monospace; 
    }
    
    /* Efecto Neón Verde Shark */
    div[data-testid="stMetricValue"] { 
        color: #00ff41 !important; 
        text-shadow: 0 0 12px #00ff41;
        font-size: 1.8rem !important;
    }
    
    h1, h2, h3 { 
        color: #00d4ff !important; 
        text-transform: uppercase;
        letter-spacing: 2px;
        border-left: 5px solid #00d4ff;
        padding-left: 15px;
    }

    .stTable { 
        background: rgba(16, 20, 30, 0.95);
        border: 1px solid #00d4ff;
        border-radius: 8px;
    }

    /* Alerta de Error Parpadeante */
    .status-error {
        background: rgba(255, 0, 60, 0.15);
        border: 1px solid #ff003c;
        padding: 15px;
        color: #ff003c;
        border-radius: 5px;
        animation: pulse 2s infinite;
    }

    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.6; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

class CyberEngine:
    def __init__(self, key, secret):
        self.key, self.secret = key, secret
        self.url = "https://api.bitso.com"

    def get_price(self, book):
        try:
            r = requests.get(f"{self.url}/v3/ticker/?book={book}", timeout=5).json()
            return float(r['payload']['last'])
        except: return 0.0

    def get_balances(self):
        if not self.key or not self.secret: return None, "MISSING_KEYS"
        path = "/v3/balances/"
        nonce = str(int(time.time() * 1000))
        message = nonce + "GET" + path
        signature = hmac.new(self.secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
        
        try:
            headers = {'Authorization': f'Bitso {self.key}:{nonce}:{signature}'}
            r = requests.get(self.url + path, headers=headers, timeout=10)
            if r.status_code == 200:
                return r.json()['payload']['balances'], "AUTHORIZED"
            return None, f"DENIED: {r.json().get('error', {}).get('message', 'Unknown Error')}"
        except: return None, "CONNECTION_OFFLINE"

bot = CyberEngine(API_KEY, API_SECRET)

# --- HEADER TÉCNICO ---
st.markdown("# 🦈 SYSTEM: SHARK_CORE_v6.1")
t_now = datetime.now().strftime('%H:%M:%S')
st.write(f"SISTEMA OPERATIVO | {t_now} | TERMINAL EN LINEA")

# --- TICKERS ---
p_usd = bot.get_price("usd_mxn") or 18.20
c1, c2, c3 = st.columns(3)
c1.metric("₿ BITCOIN", f"${bot.get_price('btc_mxn'):,.0f} MXN")
c2.metric("Ξ ETHEREUM", f"${bot.get_price('eth_mxn'):,.0f} MXN")
c3.metric("💵 USD/MXN", f"${p_usd:,.2f}")

st.divider()

# --- INTERFAZ DE DATOS ---
col_wallet, col_visual = st.columns([1.3, 2])

with col_wallet:
    st.subheader("📂 WALLET_STATUS")
    data, status = bot.get_balances()
    total_mxn = 0.0

    if status == "AUTHORIZED":
        wallet_rows = []
        for b in data:
            qty = float(b['total'])
            if qty > 0.00000001:
                coin = b['currency'].upper()
                price = 1.0 if coin == 'MXN' else bot.get_price(f"{coin.lower()}_mxn")
                if price == 0: price = bot.get_price(f"{coin.lower()}_usd") * p_usd
                
                val_mxn = qty * price
                total_mxn += val_mxn
                
                if val_mxn > 0.5:
                    wallet_rows.append({
                        "ASSET": coin,
                        "QTY": f"{qty:.6f}",
                        "VAL_MXN": f"${val_mxn:,.2f}",
                        "VAL_USD": f"${(val_mxn/p_usd):,.2f}"
                    })
        
        if wallet_rows:
            st.table(pd.DataFrame(wallet_rows))
            st.metric("NET WORTH MXN", f"${total_mxn:,.2f}")
        else:
            st.info("Billetera vacía o esperando datos...")
    else:
        st.markdown(f'<div class="status-error">🚨 ACCESS {status}</div>', unsafe_allow_html=True)
        st.write("Verifica API Key y permisos en Bitso.")

with col_visual:
    st.subheader("📉 DATA_VISUALIZATION")
    p_btc = bot.get_price("btc_mxn") or 1235000
    df = pd.DataFrame({
        'Open': [p_btc] * 20, 'High': [p_btc * 1.002] * 20, 
        'Low': [p_btc * 0.998] * 20, 'Close': [p_btc * 1.001] * 20
    })
    df.index = pd.date_range(start=datetime.now(), periods=20, freq='15min')
    
    mc = mpf.make_marketcolors(up='#00ff41', down='#ff003c', inherit=True)
    s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#161a25', facecolor='#05070a', edgecolor='#00d4ff')
    
    buf = BytesIO()
    mpf.plot(df, type='candle', style=s, figratio=(16,8), savefig=dict(fname=buf, dpi=100))
    st.image(buf, use_container_width=True)

# --- PROGRESS ---
st.divider()
target = 10000 * p_usd
progress = min(total_mxn / target, 1.0)
st.write(f"**GOAL: $10,000 USD | PROGRESS: {progress*100:.4f}%**")
st.progress(progress)
