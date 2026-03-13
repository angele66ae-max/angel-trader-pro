import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CREDENCIALES ---
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

st.set_page_config(layout="wide", page_title="SHARK NEON v7")

# --- ESTILO RGB AZUL Y MORADO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    
    .stApp { 
        background-color: #020205; 
        color: #bc13fe; 
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Títulos con Glow Morado/Azul */
    h1, h2 { 
        font-family: 'Orbitron', sans-serif;
        color: #00d4ff !important; 
        text-shadow: 0 0 15px #bc13fe, 0 0 5px #00d4ff;
        text-transform: uppercase;
        border-bottom: 2px solid #bc13fe;
    }

    /* Métricas RGB */
    div[data-testid="stMetricValue"] { 
        color: #00f2ff !important; 
        text-shadow: 0 0 10px #00f2ff;
        font-size: 2rem !important;
    }
    
    /* Tablas estilo Tron */
    .stTable { 
        background: rgba(15, 0, 30, 0.9) !important;
        border: 1px solid #bc13fe !important;
        border-radius: 10px;
        color: #00f2ff !important;
    }
    
    hr { border: 1px solid #bc13fe; }
    </style>
    """, unsafe_allow_html=True)

def get_data():
    if not API_KEY or not API_SECRET: return None, "NO_KEYS"
    # SOLUCIÓN AL 404: Definimos la URL base y el path por separado
    base_url = "https://api.bitso.com"
    path = "/v3/balances/" # Aseguramos la diagonal final
    
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + path
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    try:
        r = requests.get(base_url + path, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()['payload']['balances'], "OK"
        return None, f"Status {r.status_code}: {r.json().get('error', {}).get('message', 'Not Found')}"
    except Exception as e:
        return None, str(e)

def get_ticker(book):
    try:
        r = requests.get(f"https://api.bitso.com/v3/ticker/?book={book}").json()
        return float(r['payload']['last'])
    except: return 0.0

st.title("🦈 SHARK SYSTEM: NEON CORE v7.0")

# --- TOP BAR RGB ---
p_usd = get_ticker("usd_mxn") or 17.80
c1, c2, c3 = st.columns(3)
c1.metric("🔵 BITCOIN", f"${get_ticker('btc_mxn'):,.0f} MXN")
c2.metric("🟣 ETHEREUM", f"${get_ticker('eth_mxn'):,.0f} MXN")
c3.metric("🌐 USD/MXN", f"${p_usd:,.2f}")

st.divider()

# --- WALLET SECTION ---
st.header("🛸 STARSHIP WALLET")
balances, status = get_data()
total_mxn = 0.0

if status == "OK":
    wallet_data = []
    for b in balances:
        cant = float(b['total'])
        if cant > 0:
            coin = b['currency'].upper()
            price = 1.0 if coin == "MXN" else get_ticker(f"{coin.lower()}_mxn")
            if price == 0: price = get_ticker(f"{coin.lower()}_usd") * p_usd
            
            v_mxn = cant * price
            total_mxn += v_mxn
            
            if v_mxn > 1.0: # Solo mostramos lo que valga más de $1 peso
                wallet_data.append({
                    "ASSET": f"⚡ {coin}",
                    "BALANCE": f"{cant:.6f}",
                    "VAL_MXN": f"${v_mxn:,.2f}",
                    "VAL_USD": f"${(v_mxn/p_usd):,.2f}"
                })
    
    if wallet_data:
        st.table(pd.DataFrame(wallet_data))
        st.subheader(f"💎 TOTAL NET WORTH: ${total_mxn:,.2f} MXN")
    else:
        st.warning("Conectado, pero no se encontraron fondos.")
else:
    st.error(f"📡 ERROR DE ENLACE: {status}")
    st.info("Tip: Verifica que la URL en el código no tenga puntos extra y que la API tenga permiso de 'Balances'.")

# --- GRÁFICA RGB ---
st.divider()
st.subheader("📊 NEON MARKET STREAM")
curr_btc = get_ticker("btc_mxn") or 1234000
df = pd.DataFrame({'Open': [curr_btc]*12, 'High': [curr_btc*1.005]*12, 'Low': [curr_btc*0.995]*12, 'Close': [curr_btc]*12})
df.index = pd.date_range(start=datetime.now(), periods=12, freq='H')

# Colores de la gráfica: Azul y Morado
mc = mpf.make_marketcolors(up='#00f2ff', down='#bc13fe', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#1a1a3a', facecolor='#020205', edgecolor='#bc13fe')

buf = BytesIO()
mpf.plot(df, type='candle', style=s, figratio=(16,7), savefig=dict(fname=buf, dpi=100))
st.image(buf, use_container_width=True)
