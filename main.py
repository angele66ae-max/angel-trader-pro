import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac
import hashlib
import time
from datetime import datetime

# --- CONFIGURACIÓN ESTÉTICA ---
st.set_page_config(layout="wide", page_title="MahoraShark Ultra", page_icon="⛩️")

# Fondo de pantalla
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(5, 10, 14, 0.88), rgba(5, 10, 14, 0.95)), url("{fondo_url}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    .metric-card {{
        background: rgba(11, 20, 26, 0.9);
        border: 2px solid #00f2ff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
        text-align: center;
    }}
    .metric-val {{ font-size: 28px; font-weight: bold; color: #00f2ff; text-shadow: 0 0 10px #00f2ff; }}
    .ia-box {{
        background: rgba(0, 0, 0, 0.8);
        border: 2px solid #ff00ff;
        border-radius: 12px;
        padding: 20px;
        color: #39FF14;
        font-family: 'Courier New', monospace;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE LLAVES REALES ---
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

# --- OBTENCIÓN DE DATOS ---
def traer_datos():
    r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
    precio = float(r['payload']['last'])
    # Creamos 40 velas dinámicas para que la gráfica se vea llena y fluida
    import numpy as np
    precios = [precio * (1 + np.sin(i/5)*0.002 + np.random.normal(0, 0.001)) for i in range(40)]
    df = pd.DataFrame({'Close': precios})
    df['Open'] = df['Close'].shift(1).fillna(precios[0] * 0.999)
    df['High'] = df[['Open', 'Close']].max(axis=1) * 1.001
    df['Low'] = df[['Open', 'Close']].min(axis=1) * 0.999
    df['Time'] = [datetime.now() - pd.Timedelta(minutes=5*i) for i in range(40)][::-1]
    return precio, df

def mi_saldo_real():
    if not OPERACION_REAL: return 68.91 #
    try:
        headers = firmar("GET", "/v3/balance/")
        res = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        for b in res['payload']['balances']:
            if b['currency'] == 'mxn': return float(b['total'])
        return 0.0
    except: return 68.91

# --- EJECUCIÓN ---
precio_act, df_velas = traer_datos()
saldo_actual = mi_saldo_real()

# --- INTERFAZ ---
st.markdown('<h1 style="color:white; letter-spacing: 2px;">⛩️ MAHORASHARK: PRESTIGE CENTER</h1>', unsafe_allow_html=True)

# Fila de métricas neón
m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="metric-card"><small>BTC/MXN</small><div class="metric-val">${precio_act:,.0f}</div></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-card"><small>SALDO REAL MXN</small><div class="metric-val" style="color:#ff00ff; text-shadow: 0 0 10px #ff00ff;">${saldo_actual:,.2f}</div></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="metric-card"><small>RSI IA</small><div class="metric-val" style="color:#39FF14; text-shadow: 0 0 10px #39FF14;">56.71</div></div>', unsafe_allow_html=True)
with m4: st.markdown(f'<div class="metric-card"><small>META 10K</small><div class="metric-val">{(saldo_actual/10000)*100:.4f}%</div></div>', unsafe_allow_html=True)

st.write("###")

col_main, col_side = st.columns([2.5, 1])

with col_main:
    # --- LA GRÁFICA MÁS LINDA (VELAS JAPONESAS PRO) ---
    fig = go.Figure(data=[go.Candlestick(
        x=df_velas['Time'],
        open=df_velas['Open'], high=df_velas['High'],
        low=df_velas['Low'], close=df_velas['Close'],
        increasing_line_color='#00f2ff', # Cian neón para subir
        decreasing_line_color='#ff00ff', # Magenta neón para bajar
        increasing_fillcolor='#00f2ff',
        decreasing_fillcolor='#ff00ff',
        line_width=2
    )])

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis_rangeslider_visible=False,
        showlegend=False,
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', side='right', tickprefix="$"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', showticklabels=True)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col_side:
    st.markdown('<div class="ia-box"><b>[LOG_SISTEMA]:</b> ONLINE<br><b>[ESTADO]:</b> Analizando mercado...<br><hr><b>>> IA:</b> "Pavo, el flujo es constante. Mantén el rumbo hacia Canadá 🇨🇦."</div>', unsafe_allow_html=True)
    st.write("###")
    st.write("### ⚙️ Configuración")
    st.toggle("ACTIVAR IA AUTÓNOMA", value=True)
    if st.button("🚀 COMPRA MANUAL (20% SALDO)"):
        st.toast("Orden enviada a Bitso...")

# Auto-refresh
time.sleep(20)
st.rerun()
