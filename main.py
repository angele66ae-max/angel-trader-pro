import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac, hashlib, time
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
API_KEY = "qdgvoUmYcB"
API_SECRET = "c764dc6961cd5d1a443cbc677fe39597"

st.set_page_config(layout="wide", page_title="ANGEL PRESTIGE V42", page_icon="🏢")

# --- 2. MOTOR DE DATOS ---
def bitso_api(method, path, payload=""):
    try:
        nonce = str(int(time.time() * 1000))
        sig = hmac.new(API_SECRET.encode(), (nonce + method + path + payload).encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{sig}'}
        url = f"https://api.bitso.com{path}"
        if method == "GET": return requests.get(url, headers=headers, timeout=10).json()
        return requests.post(url, headers=headers, data=payload, timeout=10).json()
    except: return None

def cargar_todo():
    res = bitso_api("GET", "/v3/balance/")
    if res and 'payload' in res:
        bals = {b['currency']: float(b['total']) for b in res['payload']['balances']}
        return bals.get('mxn', 0.0), bals.get('btc', 0.0), True
    return 114.29, 0.00004726, False

mxn, btc, online = cargar_todo()

# --- 3. ESTILO "WALL STREET DARK" ---
st.markdown("""
<style>
    .stApp { background-color: #010409; color: #c9d1d9; font-family: 'JetBrains Mono', monospace; }
    .market-card { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; }
    .price-up { color: #238636; font-weight: bold; }
    .price-down { color: #da3633; font-weight: bold; }
    .header-alpha { background: #161b22; padding: 10px; border-bottom: 2px solid #58a6ff; display: flex; justify-content: space-around; }
</style>
""", unsafe_allow_html=True)

# --- 4. HUD ---
st.markdown(f"""
<div class="header-alpha">
    <div><small>OPERACIÓN</small><br><b>{datetime.now().strftime("%H:%M:%S")}</b></div>
    <div><small>CAPITAL DISPONIBLE</small><br><b style="color:#58a6ff">${mxn:,.2f} MXN</b></div>
    <div><small>STATUS</small><br><b style="color:#238636">● CONECTADO</b></div>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 5. EL MERCADO DE ACCIONES (COLUMNA IZQUIERDA) ---
col_acciones, col_radar, col_control = st.columns([1.2, 2.2, 1])

with col_acciones:
    st.markdown("### 🏢 MERCADO DE ACCIONES")
    
    # Simulación de visualización de empresas (Tokens de Bitso)
    empresas = [
        {"nombre": "RENDER (IA Chips)", "ticker": "RENDER", "precio": 124.50, "cambio": "+2.4%"},
        {"nombre": "SAND (Bienes Raíces)", "ticker": "SAND", "precio": 8.92, "cambio": "-1.1%"},
        {"nombre": "GALA (Entretenimiento)", "ticker": "GALA", "precio": 0.85, "cambio": "+5.2%"},
        {"nombre": "APPLE (AAPL Token)", "ticker": "AAPL", "precio": 3450.00, "cambio": "0.0%"}
    ]

    for emp in empresas:
        with st.container():
            st.markdown(f"""
            <div class="market-card">
                <small style="color:#8b949e">{emp['nombre']}</small><br>
                <span style="font-size:18px;">${emp['precio']:,}</span> 
                <span class="{'price-up' if '+' in emp['cambio'] else 'price-down'}">{emp['cambio']}</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"COMPRAR {emp['ticker']}", key=emp['ticker']):
                st.info(f"Calculando orden para {emp['ticker']}...")

with col_radar:
    st.markdown("### 📊 RADAR TÁCTICO")
    try:
        mkt = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=5).json()['payload']
        precios = [float(t['price']) for t in mkt][::-1]
        fig = go.Figure(go.Scatter(y=precios, fill='tozeroy', line=dict(color='#58a6ff', width=2)))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          height=450, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
        st.plotly_chart(fig, use_container_width=True)
    except: st.error("Señal de radar débil...")

with col_control:
    st.markdown("### 🛡️ PANEL DE MANDO")
    st.markdown('<div class="market-card" style="border-color:#da3633">', unsafe_allow_html=True)
    st.caption("SALIDA DE EMERGENCIA")
    if st.button("🚨 VENDER TODO (MXN)", use_container_width=True):
        st.warning("Liquidando activos...")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="market-card" style="border-color:#ab7df8">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:11px; color:#39FF14; font-family:monospace;">
        [LOG] >> MERCADO ACCIONES CARGADO<br>
        [LOG] >> FILTRANDO EMPRESA: RENDER<br>
        <hr style="border-color:#333">
        "Ángel, el mercado de empresas está a la izquierda. Tienes RENDER y APPLE listos para operar."
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(30)
st.rerun()
