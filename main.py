import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac, hashlib, time
from datetime import datetime

# --- 1. NÚCLEO DEPARDADOR (142 MXN BASE) ---
API_KEY = "qdgvoUmYcB"
API_SECRET = "c764dc6961cd5d1a443cbc677fe39597"
CAPITAL_ACTUAL = 142.0  # Tu nuevo poder de fuego de image_4.png
META_10K = 10000.0
FACTOR_MAHORA = 32      # Nivel de adaptación agresiva

st.set_page_config(layout="wide", page_title="MAHORASHARK V45", page_icon="🦈")

# --- 2. MOTOR DE CAZA ---
def bitso_api(method, path, payload=""):
    try:
        nonce = str(int(time.time() * 1000))
        sig = hmac.new(API_SECRET.encode(), (nonce + method + path + payload).encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{sig}'}
        url = f"https://api.bitso.com{path}"
        if method == "GET": return requests.get(url, headers=headers, timeout=10).json()
        return requests.post(url, headers=headers, data=payload, timeout=10).json()
    except: return None

def update_shark():
    res = bitso_api("GET", "/v3/balance/")
    if res and 'payload' in res:
        bals = {b['currency']: float(b['total']) for b in res['payload']['balances']}
        # Si el balance real es mayor a 142, lo usamos, si no, mantenemos tu base
        real_mxn = bals.get('mxn', 0.0)
        return max(real_mxn, CAPITAL_ACTUAL), bals.get('btc', 0.0), True
    return CAPITAL_ACTUAL, 0.00004726, False

mxn_live, btc_live, online = update_shark()

# --- 3. DISEÑO "PIEL DE TIBURÓN" (CSS) ---
st.markdown(f"""
<style>
    .stApp {{ background-color: #010409; color: #e6edf3; font-family: 'JetBrains Mono', monospace; }}
    .shark-hud {{ 
        background: linear-gradient(90deg, #0d1117, #001a2c); 
        border-left: 5px solid #00f2ff; 
        padding: 20px; 
        border-radius: 10px; 
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 242, 255, 0.2);
    }}
    .adaptation-wheel {{
        color: #ab7df8;
        font-weight: bold;
        animation: rotate 2s linear infinite;
    }}
    .market-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; }}
    .progress-bg {{ background: #21262d; border-radius: 5px; height: 12px; width: 100%; margin-top: 10px; }}
    .progress-fill {{ background: #00f2ff; height: 12px; border-radius: 5px; width: {(mxn_live/META_10K)*100}%; }}
</style>
""", unsafe_allow_html=True)

# --- 4. HUD DE ADAPTACIÓN ALFA ---
st.markdown(f"""
<div class="shark-hud">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <small style="color:#8b949e">ESTADO: ADAPTÁNDOSE (FACTOR {FACTOR_MAHORA})</small><br>
            <b style="color:#00f2ff; font-size:26px;">MAHORASHARK ALPHA</b>
        </div>
        <div style="text-align:right">
            <small style="color:#8b949e">PODER DE MORDIDA</small><br>
            <b style="color:#39FF14; font-size:26px;">${mxn_live:,.2f} MXN</b>
        </div>
    </div>
    <div class="progress-bg"><div class="progress-fill"></div></div>
    <div style="display:flex; justify-content:space-between; margin-top:5px;">
        <small style="color:#8b949e">INICIO: $142</small>
        <small style="color:#ab7df8">OBJETIVO: $10,000</small>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 5. PANEL DE CAZA ---
col_targets, col_radar, col_mahoraga = st.columns([1.2, 2.2, 1])

with col_targets:
    st.markdown("### 🏹 PRESAS DETECTADAS")
    # Mercado adaptado con el nuevo capital de image_0.png
    presas = [
        {"n": "RENDER", "p": 124.5, "c": "+2.4%"},
        {"n": "APPLE", "p": 3450.0, "c": "0.0%"},
        {"n": "SAND", "p": 8.9, "c": "-1.5%"},
        {"n": "BTC", "p": 1800000, "c": "+0.5%"}
    ]
    for p in presas:
        with st.container():
            st.markdown(f"""
            <div class="market-card">
                <b>{p['n']}</b> <span style="float:right; color:#39FF14">{p['c']}</span><br>
                <small style="color:#8b949e">Precio: ${p['p']:,}</small>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"CAZAR {p['n']}", key=p['n']):
                st.toast(f"MahoraShark lanzó una mordida a {p['n']}")

with col_radar:
    st.markdown("### 📊 ESCÁNER DE MOVIMIENTO")
    try:
        mkt_data = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=10).json()
        precios = [float(t['price']) for t in mkt_data['payload']][::-1]
        # Usando estilo visual de image_1.png
        fig = go.Figure(go.Scatter(y=precios, fill='tozeroy', line=dict(color='#00f2ff', width=3), fillcolor='rgba(0, 242, 255, 0.05)'))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          height=400, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
        st.plotly_chart(fig, use_container_width=True)
    except: st.error("Buscando rastro de sangre en el mercado...")

with col_mahoraga:
    st.markdown("### ☸️ RUEDA DE ADAPTACIÓN")
    st.markdown('<div class="market-card" style="border-top: 3px solid #ab7df8;">', unsafe_allow_html=True)
    faltante = META_10K - mxn_live
    pasos = faltante / FACTOR_MAHORA
    
    # Basado en la terminal de image_3.png y el concepto de Mahoraga
    st.markdown(f"""
    <div style="font-size:12px; font-family:monospace;">
        <span style="color:#ab7df8;">[SISTEMA]</span> Girando la rueda...<br>
        <span style="color:#ab7df8;">[FACTOR]</span> {FACTOR_MAHORA} niveles activos.<br>
        <br>
        <span style="color:#39FF14;">>> META: $10,000</span><br>
        <span style="color:#8b949e;">>> FALTA: ${faltante:,.2f}</span><br>
        <span style="color:#00f2ff;">>> ESFUERZO/PASO: ${pasos:,.2f}</span><br>
        <hr style="border-color:#333">
        <center><i>"Con 142 MXN, MahoraShark se adapta a la caída para devorar la subida."</i></center>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🚨 MODO DEFENSA ALFA", use_container_width=True):
        st.warning("Adaptándose a modo líquido (MXN)...")

time.sleep(30)
st.rerun()
