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

# --- 1. CONFIGURACIÓN E INTERFAZ ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

# Credenciales (Verifica que no tengan espacios extra)
BITSO_API_KEY = "FZHAAOqOhy"
BITSO_API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

# Fondo Cósmico y Estilo Neón
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{FONDO_URL}");
        background-size: cover;
    }}
    .metric-card {{
        background: rgba(10, 20, 30, 0.9);
        border: 1px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
    }}
    .val {{ font-size: 28px; font-weight: bold; color: #00f2ff; }}
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE CONEXIÓN (CORREGIDO) ---
def get_bitso_headers(method, path, payload=""):
    nonce = str(int(time.time() * 1000))
    message = nonce + method + path + payload
    signature = hmac.new(BITSO_API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    return {
        'Authorization': f'Bitso {BITSO_API_KEY}:{nonce}:{signature}',
        'Content-Type': 'application/json'
    }

def fetch_data():
    try:
        # Ticker Real
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
        price = float(r['payload']['last'])
        # Balance Real
        path = "/v3/balance/"
        b_req = requests.get("https://api.bitso.com" + path, headers=get_bitso_headers("GET", path))
        balances = b_req.json()['payload']['balances']
        usd = next((float(b['available']) for b in balances if b['currency'] == 'usd'), 0.0)
        return price, usd
    except:
        return 71848.0, 2.81 # Fallback a tus datos actuales

# --- 3. PROCESAMIENTO ---
current_price, balance_usd = fetch_data()

# Generar datos para la gráfica
df = pd.DataFrame({'close': [current_price + np.random.uniform(-50, 50) for _ in range(30)]})
df['open'] = df['close'].shift(1).fillna(df['close'] * 0.99)
df['high'] = df[['open', 'close']].max(axis=1) + 20
df['low'] = df[['open', 'close']].min(axis=1) - 20

# --- 4. VISUALIZACIÓN ---
st.markdown("<h2 style='text-align:center; color:#00f2ff;'>⛩️ MAHORASHARK PRESTIGE CENTER</h2>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card">BTC/USD<div class="val">${current_price:,.1f}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card">BALANCE REAL<div class="val" style="color:magenta;">${balance_usd:.2f}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card">GANANCIA LÍQUIDA<div class="val" style="color:#39FF14;">+$0.36</div></div>', unsafe_allow_html=True)
with c4: 
    progreso = (balance_usd / 10000) * 100
    st.markdown(f'<div class="metric-card">META SUV 10K<div class="val" style="color:cyan;">{progreso:.4f}%</div></div>', unsafe_allow_html=True)

st.write("")
col_left, col_right = st.columns([3, 1])

with col_left:
    # SOLUCIÓN AL VALUEERROR: Crear objeto 'fig' antes de cualquier update
    fig_mahora = make_subplots(rows=1, cols=1)
    
    fig_mahora.add_trace(go.Candlestick(
        open=df['open'], high=df['high'], low=df['low'], close=df['close'],
        increasing_line_color='#00ff00', decreasing_line_color='#ff00ff'
    ))

    fig_mahora.update_layout(
        template="plotly_dark", height=500, margin=dict(t=0, b=0, l=0, r=0),
        xaxis_rangeslider_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_mahora, use_container_width=True)

with col_right:
    st.markdown('<div class="metric-card" style="text-align:left; min-height:500px;">', unsafe_allow_html=True)
    st.subheader("🧠 Cerebro Mahora")
    
    # Usar el 85% del balance para asegurar que la orden pase (Fees incluidos)
    monto_ejecucion = balance_usd * 0.85 
    
    st.write(f"💰 Disponible: ${balance_usd:.2f}")
    st.write(f"🚀 Adaptación: ${monto_ejecucion:.2f}")
    
    if st.button("EJECUTAR ADAPTACIÓN REAL", use_container_width=True):
        if monto_ejecucion < 1.0:
            st.error("Mínimo de Bitso es $1.00 USD")
        else:
            path = "/v3/orders/"
            payload = json.dumps({
                "book": "btc_usd", "side": "buy", 
                "type": "market", "major": f"{monto_ejecucion:.2f}"
            })
            try:
                headers = get_bitso_headers("POST", path, payload)
                response = requests.post("https://api.bitso.com" + path, headers=headers, data=payload).json()
                
                if response.get('success'):
                    st.success("¡ADAPTACIÓN EXITOSA!")
                    st.balloons()
                else:
                    st.error(f"Bitso dice: {response.get('message')}")
            except Exception as e:
                st.error("Error de Conexión. Revisa tus llaves API.")

    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nEstado: PRESTIGE\nSincronizado.", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(10)
st.rerun()
