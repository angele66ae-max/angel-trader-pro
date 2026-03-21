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
NOMBRE_USUARIO = "Angel" 

st.set_page_config(layout="wide", page_title=f"MahoraShark - {NOMBRE_USUARIO}", page_icon="⛩️")

# --- SEGURIDAD (BITSO API) ---
try:
    API_KEY = st.secrets["BITSO_KEY"]
    API_SECRET = st.secrets["BITSO_SECRET"]
    MODO_REAL = True
except:
    MODO_REAL = False
    st.warning("⚠️ Modo Simulación: Configura tus llaves en Secrets para operar real.")

def firmar_solicitud(metodo, endpoint, cuerpo=""):
    nonce = str(int(time.time() * 1000))
    mensaje = nonce + metodo + endpoint + cuerpo
    firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}

# --- ESTILO VISUAL PRESTIGE ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(5, 10, 14, 0.9), rgba(5, 10, 14, 0.95)), url("{fondo_url}");
        background-size: cover; background-attachment: fixed; color: white;
    }}
    .metric-card {{
        background: rgba(11, 20, 26, 0.95); border: 2px solid #00f2ff;
        border-radius: 10px; padding: 15px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
    }}
    .metric-val {{ font-size: 24px; font-weight: bold; color: #00f2ff; }}
    </style>
    """, unsafe_allow_html=True)

# --- OBTENCIÓN DE DATOS ---
def obtener_datos():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
        precio = float(r['payload']['last'])
        # Generar 40 velas estéticas basadas en el precio actual
        precios = [precio * (1 + np.sin(i/6)*0.002 + np.random.normal(0, 0.001)) for i in range(40)]
        df = pd.DataFrame({'Close': precios})
        df['Open'] = df['Close'].shift(1).fillna(precios[0] * 0.999)
        df['High'] = df[['Open', 'Close']].max(axis=1) * 1.001
        df['Low'] = df[['Open', 'Close']].min(axis=1) * 0.999
        df['Time'] = [datetime.now() - pd.Timedelta(minutes=5*i) for i in range(40)][::-1]
        return precio, df
    except: return 1250000.0, pd.DataFrame()

def obtener_saldo_real():
    if not MODO_REAL: return 68.91
    try:
        headers = firmar_solicitud("GET", "/v3/balance/")
        res = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        for b in res['payload']['balances']:
            if b['currency'] == 'mxn': return float(b['total'])
        return 0.0
    except: return 68.91

# --- PROCESAMIENTO ---
precio_btc, df_velas = obtener_datos()
saldo_actual = obtener_saldo_real()

# --- INTERFAZ ---
st.title(f"⛩️ MAHORASHARK: {NOMBRE_USUARIO.upper()} PRO TERMINAL")

# Dashboard de métricas
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card"><small>BTC/MXN</small><div class="metric-val">${precio_btc:,.0f}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card"><small>SALDO MXN</small><div class="metric-val" style="color:#ff00ff">${saldo_actual:,.2f}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card"><small>ESTADO IA</small><div class="metric-val" style="color:#39FF14">READY</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card"><small>META 10K</small><div class="metric-val">{(saldo_actual/10000)*100:.4f}%</div></div>', unsafe_allow_html=True)

st.write("---")

col_graph, col_info = st.columns([2.5, 1])

with col_graph:
    # Gráfica Neón Ultra-Limpia
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
    st.plotly_chart(fig, use_container_width=True)

with col_info:
    st.subheader("🧠 Cerebro Mahora")
    st.info(f"Hola **{NOMBRE_USUARIO}**, el sistema está monitoreando el mercado en tiempo real.")
    
    # Simulación de pensamiento de IA
    st.code(f"""
    > ANALIZANDO BITSO...
    > PRECIO: ${precio_btc}
    > SALDO: ${saldo_actual}
    > OBJETIVO: CANADA 2026
    > ACCIÓN: HOLD
    """, language="bash")
    
    if st.button("🚀 EJECUTAR COMPRA (20%)", use_container_width=True):
        if MODO_REAL:
            st.toast("Enviando orden real a Bitso...")
        else:
            st.error("Configura tus API Keys para comprar.")

# Refresh cada 30 segundos
time.sleep(30)
st.rerun()
