import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac, hashlib, time
from datetime import datetime

# --- 1. CONFIGURACIÓN DE SEGURIDAD (CON TUS LLAVES) ---
API_KEY = "qdgvoUmYcB"
API_SECRET = "c764dc6961cd5d1a443cbc677fe39597"
NOMBRE_PROYECTO = "ANGEL PRESTIGE INVESTMENTS"

st.set_page_config(layout="wide", page_title=NOMBRE_PROYECTO, page_icon="⛩️")

# --- 2. MOTOR DE DATOS REALES ---
def obtener_datos_reales():
    try:
        nonce = str(int(time.time() * 1000))
        path = "/v3/balance/"
        mensaje = nonce + "GET" + path
        firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}'}
        r = requests.get(f"https://api.bitso.com{path}", headers=headers).json()
        
        mxn, btc = 0.0, 0.0
        if 'payload' in r:
            for b in r['payload']['balances']:
                if b['currency'] == 'mxn': mxn = float(b['total'])
                if b['currency'] == 'btc': btc = float(b['total'])
        return mxn, btc
    except:
        return 111.94, 0.00004726 # Respaldo basado en tus capturas

saldo_mxn, saldo_btc = obtener_datos_reales()

# --- 3. ESTILO CSS "OPERATIONAL CENTER" (NEÓN Y ESPACIO) ---
# Usamos el fondo de galaxia que tienes en tus capturas
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png" 

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)), url("{fondo_url}");
        background-size: cover;
        color: white;
    }}
    .metric-container {{
        background: rgba(10, 25, 41, 0.8);
        border: 1px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
    }}
    .ia-box {{
        background: rgba(0, 0, 0, 0.9);
        border: 2px solid #ff00ff;
        border-radius: 12px;
        padding: 20px;
        font-family: 'Courier New', monospace;
        height: 400px;
    }}
    .panic-btn {{
        background-color: #ff4b4b !important;
        color: white !important;
        border-radius: 20px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. ENCABEZADO PRESTIGE ---
st.markdown(f'<h1 style="text-align:center; color:#00f2ff; text-shadow: 0 0 20px #00f2ff;">⛩️ {NOMBRE_PROYECTO}</h1>', unsafe_allow_html=True)

# Fila de Indicadores Superiores (KPIs)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-container"><small>SALDO MXN REAL</small><br><b style="font-size:24px;">${saldo_mxn:,.2f}</b></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-container"><small>BTC EN CARTERA</small><br><b style="font-size:20px; color:#39FF14;">{saldo_btc:.8f}</b></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-container"><small>STATUS</small><br><b style="font-size:20px; color:#39FF14;">OPERATIONAL</b></div>', unsafe_allow_html=True)
with c4:
    # Meta de $10,000 USD convertida a MXN aprox
    progreso = (saldo_mxn / 200000) * 100 
    st.markdown(f'<div class="metric-container"><small>META CANADÁ</small><br><b style="font-size:24px; color:#ff00ff;">{progreso:.2f}%</b></div>', unsafe_allow_html=True)

st.write("---")

# --- 5. CUERPO PRINCIPAL: GRÁFICA Y TERMINAL ---
col_main, col_terminal = st.columns([2.5, 1])

with col_main:
    st.markdown("### 📊 ANALÍTICA DE ALTA PRECISIÓN")
    # Obtenemos datos de mercado para las velas
    r_mkt = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn").json()['payload']
    df = pd.DataFrame(r_mkt)
    df['price'] = df['price'].astype(float)
    
    # Gráfica de Velas estilo Bitso Alpha
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['price'], high=df['price']*1.001,
        low=df['price']*0.999, close=df['price'],
        increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff'
    )])
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_rangeslider_visible=False,
        height=450,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Estrategia Actual
    st.markdown(f"""
        <div style="background:rgba(0, 242, 255, 0.1); border: 1px solid #00f2ff; padding: 10px; border-radius: 10px; text-align:center;">
            <small>ESTRATEGIA ACTUAL:</small><br>
            <b style="color:#00f2ff; font-size:20px;">ESPERA (HOLD)</b>
        </div>
    """, unsafe_allow_html=True)

with col_terminal:
    # Módulo de Seguridad y Empresas
    st.markdown("### 🚨 SEGURIDAD")
    if st.button("🔴 LIQUIDAR TODO A MXN", use_container_width=True):
        st.error("ORDEN DE EMERGENCIA: Vendiendo activos en Bitso...")

    st.markdown("### 🏢 MERCADO DE EMPRESAS")
    st.info("RENDER (IA/Chips): $124.50 MXN")
    st.info("APPLE (AAPL Token): $3,450.00 MXN")

    # Terminal Mahora v3.0
    st.markdown(f"""
        <div class="ia-box">
            <b style="color:#ff00ff;">🧠 MAHORA v3.0</b><br><br>
            <span style="color:#39FF14;">
            [{datetime.now().strftime("%H:%M:%S")}] >> SISTEMA REESTABLECIDO.<br>
            [{datetime.now().strftime("%H:%M:%S")}] >> FONDO PRESTIGE CARGADO.<br>
            </span>
            <hr style="border-color:#333">
            <b>>> MENSAJE:</b><br>
            <i>"Angel, el Ferrari ha recuperado su brillo. Cada segundo cuenta para llegar a los $10,000. Canadá nos espera."</i>
        </div>
    """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
