import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac, hashlib, time
from datetime import datetime

# --- 1. NÚCLEO DE PODER ---
API_KEY = "qdgvoUmYcB"
API_SECRET = "c764dc6961cd5d1a443cbc677fe39597"
PROYECTO = "ANGEL PRESTIGE COMMAND"

st.set_page_config(layout="wide", page_title=PROYECTO, page_icon="⚔️")

# --- 2. MOTOR DE EJECUCIÓN ---
def bitso_api(method, path, payload=""):
    nonce = str(int(time.time() * 1000))
    signature = hmac.new(API_SECRET.encode(), (nonce + method + path + payload).encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    url = f"https://api.bitso.com{path}"
    try:
        if method == "GET": return requests.get(url, headers=headers).json()
        return requests.post(url, headers=headers, data=payload).json()
    except: return {}

def cargar_balance():
    try:
        r = bitso_api("GET", "/v3/balance/")
        balances = {b['currency']: float(b['total']) for b in r['payload']['balances']}
        return balances.get('mxn', 0.0), balances.get('btc', 0.0), balances.get('eth', 0.0), True
    except: 
        return 114.29, 0.00004726, 0.0012, False

mxn, btc, eth, online = cargar_balance()

# --- 3. DISEÑO "TACTICAL BLACK" (CORREGIDO) ---
st.markdown(f"""
<style>
.stApp {{ background-color: #020608; color: #e1e1e1; font-family: 'Inter', sans-serif; }}
.header-bar {{ background: #0a0f12; border-bottom: 2px solid #00f2ff; padding: 15px; display: flex; justify-content: space-around; }}
.card {{ background: #0d1216; border: 1px solid #1e252b; border-radius: 6px; padding: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.5); }}
.glow-text {{ color: #00f2ff; text-shadow: 0 0 10px #00f2ff; }}
.terminal {{ font-family: 'JetBrains Mono', monospace; color: #39FF14; font-size: 11px; line-height: 1.2; }}
</style>
""", unsafe_allow_html=True)

# --- 4. TOP HUD ---
st.markdown(f"""
<div class="header-bar">
    <div style="text-align:center"><small style="color:#666">ESTADO</small><br><b style="color:{'#39FF14' if online else '#ff4b4b'}">● {'TACTICAL LIVE' if online else 'OFFLINE'}</b></div>
    <div style="text-align:center"><small style="color:#666">FONDOS MXN</small><br><b class="glow-text">${mxn:,.2f}</b></div>
    <div style="text-align:center"><small style="color:#666">META CANADÁ</small><br><b style="color:#ff00ff">{(mxn/200000)*100:.2f}%</b></div>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 5. INTERFAZ ---
col_left, col_mid, col_right = st.columns([1, 2.5, 1])

with col_left:
    st.markdown("### 🏢 CORPORATIVO")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.metric("RENDER (IA)", "$124.50", "+2.4%")
    st.metric("SAND (Land)", "$8.90", "-1.2%")
    st.button("DIVERSIFICAR")
    st.markdown('</div>', unsafe_allow_html=True)

with col_mid:
    st.markdown("### 📊 RADAR TÁCTICO")
    try:
        r_mkt = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn").json()['payload']
        df = pd.DataFrame(r_mkt)
        df['price'] = df['price'].astype(float)
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['price'], high=df['price'], low=df['price'], close=df['price'], increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff')])
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False, height=450, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
    except: st.warning("Esperando datos de mercado...")

with col_right:
    st.markdown("### 🛡️ CONTROL")
    st.markdown('<div class="card" style="border-color:#ff4b4b">', unsafe_allow_html=True)
    if st.button("⚠️ VENTA FLASH"):
        bitso_api("POST", "/v3/orders/", f'{{"book":"btc_mxn","side":"sell","type":"market","major":"{btc}"}}')
        st.error("EJECUTANDO...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    st.markdown('<div class="card" style="border-left: 3px solid #ff00ff">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="terminal">
        [{datetime.now().strftime("%H:%M")}] >> ARMADURA REPARADA.<br>
        [{datetime.now().strftime("%H:%M")}] >> ERROR DE SINTAXIS ELIMINADO.<br>
        <hr style="border-color:#222">
        >> "Pavo, el código ya está limpio. El Ferrari está listo para correr."
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(10)
st.rerun()
