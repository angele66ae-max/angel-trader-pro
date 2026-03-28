import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac, hashlib, time
from datetime import datetime

# --- 1. NÚCLEO DE ADAPTACIÓN (MAHORASHARK CORE) ---
API_KEY = "qdgvoUmYcB"
API_SECRET = "c764dc6961cd5d1a443cbc677fe39597"
META_FINAL = 10000.0

st.set_page_config(layout="wide", page_title="MAHORASHARK V44", page_icon="⚔️")

# --- 2. MOTOR DE EJECUCIÓN ---
def bitso_cmd(method, path, payload=""):
    try:
        nonce = str(int(time.time() * 1000))
        sig = hmac.new(API_SECRET.encode(), (nonce + method + path + payload).encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{sig}'}
        url = f"https://api.bitso.com{path}"
        if method == "GET": return requests.get(url, headers=headers, timeout=10).json()
        return requests.post(url, headers=headers, data=payload, timeout=10).json()
    except: return None

def sync_data():
    res = bitso_cmd("GET", "/v3/balance/")
    if res and 'payload' in res:
        bals = {b['currency']: float(b['total']) for b in res['payload']['balances']}
        return bals.get('mxn', 0.0), bals.get('btc', 0.0), True
    return 114.29, 0.00004726, False

mxn, btc, online = sync_data()

# --- 3. DISEÑO "GUADAÑA ADAPTATIVA" (CSS) ---
st.markdown(f"""
<style>
    .stApp {{ background-color: #010409; color: #e6edf3; font-family: 'JetBrains Mono', monospace; }}
    .scythe-hud {{ background: linear-gradient(90deg, #0d1117, #1f1f1f); border-left: 5px solid #ab7df8; padding: 15px; border-radius: 0 10px 10px 0; margin-bottom: 20px; }}
    .market-box {{ background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 8px; border-right: 3px solid #ab7df8; }}
    .terminal-green {{ color: #39FF14; font-size: 11px; }}
    .progress-bar {{ background: #21262d; border-radius: 10px; height: 10px; width: 100%; }}
    .progress-fill {{ background: #ab7df8; height: 10px; border-radius: 10px; width: {(mxn/META_FINAL)*100}%; }}
</style>
""", unsafe_allow_html=True)

# --- 4. HUD DE PODER: RUMBO A 10K ---
st.markdown(f"""
<div class="scythe-hud">
    <div style="display:flex; justify-content:space-between;">
        <div><small style="color:#8b949e">GUADAÑA ACTIVADA</small><br><b style="color:#ab7df8; font-size:22px;">MAHORASHARK V44</b></div>
        <div style="text-align:right"><small style="color:#8b949e">CAPITAL ACTUAL</small><br><b style="color:#58a6ff; font-size:22px;">${mxn:,.2f} MXN</b></div>
    </div>
    <div style="margin-top:10px;">
        <small style="color:#8b949e">PROGRESO HACIA META 10K</small>
        <div class="progress-bar"><div class="progress-fill"></div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 5. ESPACIO DE CAZA ---
col_inv, col_radar, col_ai = st.columns([1.3, 2.2, 1])

with col_inv:
    st.markdown("### 🏢 ADAPTACIÓN: EMPRESAS")
    # Arsenal de compra de MahoraShark
    targets = [
        {"n": "RENDER (IA)", "t": "RENDER", "p": 124.50, "v": "+2.4%"},
        {"n": "APPLE (AAPL)", "t": "AAPL", "p": 3450.00, "v": "-0.1%"},
        {"n": "SAND (Land)", "t": "SAND", "p": 8.92, "v": "-1.5%"},
        {"n": "GALA (Games)", "t": "GALA", "p": 0.85, "v": "+4.2%"}
    ]
    
    for t in targets:
        with st.container():
            st.markdown(f"""
            <div class="market-box">
                <div style="display:flex; justify-content:space-between;">
                    <b>{t['n']}</b>
                    <span style="color:{'#238636' if '+' in t['v'] else '#da3633'}">{t['v']}</span>
                </div>
                <small style="color:#8b949e">${t['p']:,} MXN</small>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"ADAPTAR & COMPRAR {t['t']}", key=t['t']):
                st.toast(f"MahoraShark detectó oportunidad en {t['t']}")

with col_radar:
    st.markdown("### 📊 RADAR TÁCTICO")
    try:
        m_req = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=10).json()
        prices = [float(t['price']) for t in m_req['payload']][::-1]
        fig = go.Figure(go.Scatter(y=prices, fill='tozeroy', line=dict(color='#ab7df8', width=3), fillcolor='rgba(171, 125, 248, 0.1)'))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          height=450, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
        st.plotly_chart(fig, use_container_width=True)
    except: st.error("Buscando debilidad en el mercado...")

with col_ai:
    st.markdown("### 🧠 CEREBRO")
    st.markdown('<div class="market-box" style="border-color:#da3633; border-right:none; border-left:3px solid #da3633">', unsafe_allow_html=True)
    if st.button("🚨 LIQUIDAR TODO", use_container_width=True):
        st.error("MAHORA ADAPTÁNDOSE A MXN (PÁNICO)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="market-box">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="terminal-green">
        [{datetime.now().strftime("%H:%M")}] >> OBJETIVO: 10,000 MXN<br>
        [{datetime.now().strftime("%H:%M")}] >> MODO: ADAPTACIÓN TOTAL<br>
        <hr style="border-color:#333">
        "Ángel, la guadaña está lista. MahoraShark no se detendrá hasta que tu balance marque los 10K."
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(30)
st.rerun()
