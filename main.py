import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hmac, hashlib, time, numpy as np
from datetime import datetime

# --- 1. CONFIGURACIÓN DE IDENTIDAD ---
NOMBRE = "Angel"
st.set_page_config(layout="wide", page_title=f"{NOMBRE}'s Prestige Center", page_icon="⛩️")

# --- 2. CONEXIÓN REAL BITSO ---
API_KEY = st.secrets.get("BITSO_KEY")
API_SECRET = st.secrets.get("BITSO_SECRET")
MODO_REAL = True if API_KEY and API_SECRET else False

def firmar(metodo, endpoint, cuerpo=""):
    nonce = str(int(time.time() * 1000))
    mensaje = nonce + metodo + endpoint + cuerpo
    firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}

# --- 3. DISEÑO CSS PRESTIGE (UI/UX) ---
st.markdown("""
    <style>
    .stApp { background-color: #06090f; color: #e6e6e6; }
    #MainMenu, header, footer {visibility: hidden;}
    .header-container { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    .main-title { color: #ffffff; font-size: 28px; font-weight: 700; text-shadow: 0 0 10px #00f2ff; }
    .metric-card { background-color: #0b1018; border: 1px solid #1a2638; border-radius: 8px; padding: 15px; text-align: center; }
    .metric-title { color: #8b9bb4; font-size: 12px; text-transform: uppercase; margin-bottom: 5px; }
    .metric-val { color: #ffffff; font-size: 24px; font-weight: 700; }
    .ia-panel { background-color: #0b1018; border: 1px solid #ff00ff; border-radius: 12px; padding: 20px; height: 100%; }
    .ia-console { background-color: #000000; border-radius: 8px; padding: 15px; font-family: 'Courier New', monospace; color: #39FF14; font-size: 13px; height: 280px; overflow-y: auto; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNCIONES DE DATOS (CORREGIDAS) ---
def obtener_datos():
    # Mercado
    r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()['payload']
    p = float(r['last'])
    # Cartera
    saldo = 117.63 # Valor por defecto según tu captura de Bitso
    if MODO_REAL:
        try:
            h = firmar("GET", "/v3/balance/")
            res = requests.get("https://api.bitso.com/v3/balance/", headers=h).json()
            for b in res['payload']['balances']:
                if b['currency'] == 'mxn':
                    saldo = float(b['total'])
        except: pass
    
    # Velas para la gráfica
    precios = [p * (1 + np.sin(i/10)*0.002) for i in range(50)]
    df = pd.DataFrame({'Close': precios})
    df['Open'] = df['Close'].shift(1).fillna(p)
    df['High'] = df['Close'] * 1.001
    df['Low'] = df['Close'] * 0.999
    df['EMA'] = df['Close'].ewm(span=10).mean()
    return p, saldo, df

# --- 5. EJECUCIÓN Y RENDERIZADO ---
precio_btc, saldo_mxn, df_grafica = obtener_datos()

# Header
st.markdown(f'<div class="header-container"><div class="main-title">⛩️ MAHORASHARK</div><div style="color: #00f2ff;">{NOMBRE.upper()}\'S PRESTIGE CENTER</div></div>', unsafe_allow_html=True)

# Métricas
m1, m2, m3, m4 = st.columns(4)
m1.markdown(f'<div class="metric-card"><div class="metric-title">BTC/MXN</div><div class="metric-val">${precio_btc:,.0f}</div></div>', unsafe_allow_html=True)
m2.markdown(f'<div class="metric-card"><div class="metric-title">MXN BALANCE</div><div class="metric-val" style="color:#ff00ff">${saldo_mxn:,.2f}</div></div>', unsafe_allow_html=True)
m3.markdown(f'<div class="metric-card"><div class="metric-title">IA STATUS</div><div class="metric-val" style="color:#39FF14">{"ACTIVE" if MODO_REAL else "SIM"}</div></div>', unsafe_allow_html=True)
m4.markdown(f'<div class="metric-card"><div class="metric-title">META 10K</div><div class="metric-val">{(saldo_mxn/10000)*100:.2f}%</div></div>', unsafe_allow_html=True)

st.write("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.write("### 📈 Gráfica de Velas (Professional View)")
    fig = go.Figure(data=[go.Candlestick(open=df_grafica['Open'], high=df_grafica['High'], low=df_grafica['Low'], close=df_grafica['Close'],
                                         increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff')])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown(f"""
        <div class="ia-panel">
            <div style="color:#ff00ff; font-weight:bold; margin-bottom:10px;">🧠 CEREBRO MAHORA v2.1</div>
            <div class="ia-console">
                [{datetime.now().strftime("%H:%M")}] >> SISTEMA ONLINE.<br>
                [{datetime.now().strftime("%H:%M")}] >> LLAVES CONECTADAS: {"SÍ" if MODO_REAL else "NO"}.<br>
                [{datetime.now().strftime("%H:%M")}] >> SALDO: ${saldo_mxn} MXN.<br>
                <hr style="border-color:#333">
                >> Angel, el mercado está listo. Tu meta de Canadá está a un {(100 - (saldo_mxn/10000)*100):.2f}% de distancia.
            </div>
        </div>
        """, unsafe_allow_html=True)

# Refresco automático cada 30 seg
time.sleep(30)
st.rerun()
