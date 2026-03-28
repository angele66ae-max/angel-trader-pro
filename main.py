import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac, hashlib, time
from datetime import datetime

# --- 1. ADN DEL SISTEMA ---
API_KEY = "qdgvoUmYcB"
API_SECRET = "c764dc6961cd5d1a443cbc677fe39597"

st.set_page_config(layout="wide", page_title="ANGEL PRESTIGE V43", page_icon="⚡")

# --- 2. MOTOR DE EJECUCIÓN ---
def bitso_command(method, path, payload=""):
    try:
        nonce = str(int(time.time() * 1000))
        sig = hmac.new(API_SECRET.encode(), (nonce + method + path + payload).encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{sig}'}
        url = f"https://api.bitso.com{path}"
        if method == "GET": return requests.get(url, headers=headers, timeout=10).json()
        return requests.post(url, headers=headers, data=payload, timeout=10).json()
    except: return None

def update_system():
    res = bitso_command("GET", "/v3/balance/")
    if res and 'payload' in res:
        bals = {b['currency']: float(b['total']) for b in res['payload']['balances']}
        return bals.get('mxn', 0.0), bals.get('btc', 0.0), True
    return 114.29, 0.00004726, False

mxn, btc, status = update_system()

# --- 3. ESTILO DE ALTA PRECISIÓN (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #010409; color: #e6edf3; font-family: 'JetBrains Mono', monospace; }
    .hud-top { background: #0d1117; border-bottom: 2px solid #58a6ff; padding: 10px 20px; display: flex; justify-content: space-between; border-radius: 0 0 10px 10px; }
    .card-dark { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; margin-bottom: 10px; }
    .stock-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #21262d; }
    .btn-buy { background: #238636 !important; color: white !important; border: none !important; font-size: 10px !important; }
</style>
""", unsafe_allow_html=True)

# --- 4. HUD DE COMANDO ---
st.markdown(f"""
<div class="hud-top">
    <div><small style="color:#8b949e">TERMINAL</small><br><b>ANGEL_V43_PRIME</b></div>
    <div><small style="color:#8b949e">CAPITAL REAL</small><br><b style="color:#58a6ff">${mxn:,.2f} MXN</b></div>
    <div><small style="color:#8b949e">META CANADÁ</small><br><b style="color:#ab7df8">{(mxn/200000)*100:.2f}%</b></div>
    <div><small style="color:#8b949e">ESTADO</small><br><b style="color:#238636">● ACTIVE</b></div>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 5. INTERFAZ MARTILLADA (ELGADA Y EFICIENTE) ---
col_stocks, col_radar, col_control = st.columns([1.3, 2.2, 1])

with col_stocks:
    st.markdown("### 🏢 STOCK MARKET")
    st.markdown('<div class="card-dark">', unsafe_allow_html=True)
    
    # Lista de Empresas/Tokens
    stocks = [
        {"n": "RENDER (IA)", "t": "render_mxn", "p": 124.50, "c": "+2.4%"},
        {"n": "APPLE (AAPL)", "t": "aapl_mxn", "p": 3450.00, "c": "-0.1%"},
        {"n": "SAND (Land)", "t": "sand_mxn", "p": 8.92, "c": "-1.5%"},
        {"n": "GALA (Games)", "t": "gala_mxn", "p": 0.85, "c": "+4.2%"}
    ]
    
    for s in stocks:
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"**{s['n']}**<br><small style='color:#8b949e'>${s['p']:,}</small> <small style='color:#238636'>{s['c']}</small>", unsafe_allow_html=True)
        if c2.button("BUY", key=s['t']):
            st.toast(f"Abriendo orden para {s['n']}...")
    st.markdown('</div>', unsafe_allow_html=True)

with col_radar:
    st.markdown("### 📊 RADAR TÁCTICO")
    try:
        m_req = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=10).json()
        prices = [float(t['price']) for t in m_req['payload']][::-1]
        fig = go.Figure(go.Scatter(y=prices, fill='tozeroy', line=dict(color='#58a6ff', width=2), fillcolor='rgba(88,166,255,0.05)'))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          height=450, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
        st.plotly_chart(fig, use_container_width=True)
    except: st.error("Buscando señal de mercado...")

with col_control:
    st.markdown("### 🛡️ CONTROL")
    st.markdown('<div class="card-dark" style="border-color:#da3633">', unsafe_allow_html=True)
    if st.button("🚨 LIQUIDAR TODO", use_container_width=True):
        bitso_command("POST", "/v3/orders/", f'{{"book":"btc_mxn","side":"sell","type":"market","major":"{btc}"}}')
        st.error("VENTA DE EMERGENCIA")
    st.markdown('</div>', unsafe_allow_
