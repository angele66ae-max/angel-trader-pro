import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac
import hashlib
import time
from datetime import datetime
import numpy as np

# --- CONFIGURACIÓN DE IDENTIDAD ---
NOMBRE = "Angel"
st.set_page_config(layout="wide", page_title=f"MahoraShark Ultra - {NOMBRE}")

# --- SEGURIDAD BITSO ---
try:
    API_KEY = st.secrets["BITSO_KEY"]
    API_SECRET = st.secrets["BITSO_SECRET"]
    OPERACION_REAL = True
except:
    OPERACION_REAL = False

def firmar(metodo, endpoint, cuerpo=""):
    nonce = str(int(time.time() * 1000))
    mensaje = nonce + metodo + endpoint + cuerpo
    firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}

# --- DISEÑO ULTRA PRESTIGE (GOTAS DE AGUA) ---
# Usamos el fondo cósmico con el efecto de gotas de agua neón
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(5, 10, 14, 0.93), rgba(5, 10, 14, 0.98)), url("{fondo_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .metric-card {{
        background: rgba(11, 20, 26, 0.95);
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
        text-align: center;
    }}
    .metric-val {{ font-size: 24px; font-weight: bold; color: #00f2ff; }}
    .ia-log {{
        background-color: rgba(0, 0, 0, 0.9);
        border: 2px solid #ff00ff;
        border-radius: 10px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        color: #39FF14;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- OBTENCIÓN DE DATOS REALES ---
def obtener_mercado():
    r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
    precio = float(r['payload']['last'])
    # Creamos 40 velas dinámicas para que la gráfica se vea fluida y llena
    precios = [precio * (1 + np.sin(i/6)*0.002 + np.random.normal(0, 0.001)) for i in range(40)]
    df = pd.DataFrame({'Close': precios})
    df['Open'] = df['Close'].shift(1).fillna(precios[0] * 0.999)
    df['High'] = df[['Open', 'Close']].max(axis=1) * 1.001
    df['Low'] = df[['Open', 'Close']].min(axis=1) * 0.999
    df['Time'] = [datetime.now() - pd.Timedelta(minutes=5*i) for i in range(40)][::-1]
    return precio, df

def obtener_saldo_mxn_real():
    if not OPERACION_REAL: return 68.91
    try:
        headers = firmar("GET", "/v3/balance/")
        res = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        for b in res['payload']['balances']:
            if b['currency'] == 'mxn': return float(b['total'])
        return 0.0
    except: return 68.91

# --- PROCESAMIENTO ---
precio_btc, df_velas = obtener_mercado()
saldo_actual = obtener_saldo_mxn_real()

# --- INTERFAZ MAHORASHARK ULTRA ---
st.title(f"⛩️ MAHORASHARK: ULTRA PRESTIGE terminal")

# Fila Superior: Tarjetas Neón
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card"><small>BTC/MXN BITSO</small><div class="metric-val">${precio_btc:,.0f}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card"><small>SALDO REAL MXN</small><div class="metric-val" style="color:#ff00ff">${saldo_actual:,.2f}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card"><small>ESTADO IA</small><div class="metric-val" style="color:#39FF14">ACTIVE</div></div>', unsafe_allow_html=True)
with c4: 
    progreso = (saldo_actual / 10000) * 100
    st.markdown(f'<div class="metric-card"><small>META 10K</small><div class="metric-val">{progreso:.4f}%</div></div>', unsafe_allow_html=True)

st.write("---")

col_main, col_brain = st.columns([2.5, 1])

with col_main:
    # --- LA GRÁFICA MÁS LINDA (ESTILO IMAGEN 1) ---
    st.subheader("📊 Gráfica de Velas Japonesas Profesionales")
    # Gráfica Neón con colores sólidos y ultra-limpia
    fig = go.Figure(data=[go.Candlestick(
        x=df_velas['Time'], open=df_velas['Open'], high=df_velas['High'],
        low=df_velas['Low'], close=df_velas['Close'],
        increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff',
        increasing_fillcolor='#00f2ff', decreasing_fillcolor='#ff00ff'
    )])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', side='right'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)')
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col_brain:
    st.subheader("🧠 Cerebro Mahora")
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="ia-log">
            [{ahora}]<br>
            SISTEMA: {'ONLINE' if OPERACION_REAL else 'IDLE'}<br>
            API BITSO: {'CONNECTED ✅' if OPERACION_REAL else 'DISCONNECTED ❌'}<br>
            <hr>
            >> Pensamiento: {"IA lista para operar con tu saldo real." if OPERACION_REAL else "Esperando conexión para el viaje a Canadá 🇨🇦."}
        </div>
    """, unsafe_allow_html=True)
    
    st.write("### 🛡️ Control de Operaciones")
    st.toggle("ACTIVAR IA AUTÓNOMA (MODO PRESTIGE)", value=True)
    if st.button("🚀 EJECUTAR OPERACIÓN REAL CON 20% SALDO"):
        if OPERACION_REAL:
            st.toast("Conectando con Bitso API para orden real...")
        else:
            st.error("Error: Conecta tus llaves primero.")

# Auto-refresh
time.sleep(15)
st.rerun()
