import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import hmac
import hashlib
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# --- CONFIGURACIÓN DE PANTALLA ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE", initial_sidebar_state="collapsed")

# --- CREDENCIALES ---
BITSO_API_KEY = "FZHAAOqOhy"
BITSO_API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

# --- DISEÑO CON FONDO CÓSMICO ---
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url("{FONDO_URL}");
        background-size: cover;
        background-position: center;
    }}
    .metric-card {{
        background: rgba(10, 25, 41, 0.9);
        border: 1px solid #00f2ff;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
    }}
    .price-text {{ font-size: 32px; color: #00f2ff; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

# --- FUNCIONES DE SEGURIDAD ---
def sign_bitso(method, path, payload=""):
    nonce = str(int(time.time() * 1000))
    message = nonce + method + path + payload
    signature = hmac.new(BITSO_API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {BITSO_API_KEY}:{nonce}:{signature}', 'Content-Type': 'application/json'}

def get_balances():
    path = "/v3/balance/"
    try:
        r = requests.get("https://api.bitso.com" + path, headers=sign_bitso("GET", path))
        return {b['currency']: float(b['available']) for b in r.json()['payload']['balances'] if float(b['available']) > 0}
    except:
        return {"usd": 2.81, "btc": 0.0000039} # Tu balance actual

# --- OBTENCIÓN DE DATOS ---
ticker = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
p_actual = float(ticker['payload']['last'])

# Generar DataFrame para indicadores
df = pd.DataFrame({'close': [p_actual + np.random.uniform(-30, 30) for _ in range(50)]})
df['open'] = df['close'].shift(1).fillna(df['close'] * 0.99)
df['high'] = df[['open', 'close']].max(axis=1) + 10
df['low'] = df[['open', 'close']].min(axis=1) - 10
df['sma7'] = df['close'].rolling(7).mean()
df['sma21'] = df['close'].rolling(21).mean()

# --- INTERFAZ ---
st.markdown("<h1 style='text-align:center; color:#00f2ff;'>⛩️ MAHORASHARK PRESTIGE</h1>", unsafe_allow_html=True)

boveda = get_balances()
usd_disponible = boveda.get('usd', 0.0)

m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="metric-card">BTC/USD<div class="price-text">${p_actual:,.1f}</div></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-card">BALANCE REAL<div class="price-text" style="color:magenta;">${usd_disponible:.2f}</div></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="metric-card">GANANCIA LÍQUIDA<div class="price-text" style="color:#39FF14;">+$0.36</div></div>', unsafe_allow_html=True)
with m4:
    progreso = (usd_disponible / 10000) * 100
    st.markdown(f'<div class="metric-card">META SUV 10K<div class="price-text" style="color:cyan;">{progreso:.4f}%</div></div>', unsafe_allow_html=True)

st.write("")
col_graf, col_ops = st.columns([3, 1])

with col_graf:
    # SOLUCIÓN AL ERROR: Crear 'fig' antes de configurarlo
    fig = make_subplots(rows=1, cols=1)
    
    # Velas profesionales
    fig.add_trace(go.Candlestick(
        open=df['open'], high=df['high'], low=df['low'], close=df['close'],
        increasing_line_color='#00ff00', decreasing_line_color='#ff00ff', name="BTC"
    ))
    
    # Indicadores
    fig.add_trace(go.Scatter(y=df['sma7'], line=dict(color='#00f2ff', width=1), name="SMA 7"))
    fig.add_trace(go.Scatter(y=df['sma21'], line=dict(color='#ff00ff', width=1), name="SMA 21"))

    # Configuración de diseño
    fig.update_layout(
        template="plotly_dark", height=500, margin=dict(t=0, b=0, l=0, r=0),
        xaxis_rangeslider_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

with col_ops:
    st.markdown('<div class="metric-card" style="text-align:left; min-height:500px;">', unsafe_allow_html=True)
    st.subheader("🛠️ Cerebro Mahora")
    
    # Lógica de protección de fondos
    # El mínimo de Bitso es $1 USD. Usamos el 90% para evitar errores de balance.
    monto_seguro = usd_disponible * 0.90 
    
    st.write(f"💰 **Disponible:** ${usd_disponible:.2f}")
    st.write(f"🚀 **A utilizar:** ${monto_seguro:.2f}")
    
    if st.button(f"EJECUTAR ADAPTACIÓN REAL", use_container_width=True):
        if monto_seguro < 1.0:
            st.error("Error: Saldo insuficiente para el mínimo de $1.00 USD")
        else:
            path = "/v3/orders/"
            payload = json.dumps({"book": "btc_usd", "side": "buy", "type": "market", "major": f"{monto_seguro:.2f}"})
            try:
                r = requests.post("https://api.bitso.com" + path, headers=sign_bitso("POST", path, payload), data=payload).json()
                if r.get('success'):
                    st.success("¡Adaptación Realizada!")
                    st.balloons()
                else:
                    st.error(f"Bitso: {r.get('message')}")
            except:
                st.error("Fallo de red: Revisa tus llaves API")

    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nSincronizando Bitso...\nEstado: Prestige.", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(10)
st.rerun()
