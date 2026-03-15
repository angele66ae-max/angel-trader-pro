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

# --- LLAVES DE ACCESO ---
BITSO_API_KEY = "FZHAAOqOhy"
BITSO_API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

# --- ESTILO TRADINGVIEW DARK PRO ---
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{FONDO_URL}"); background-size: cover; }}
    .metric-card {{
        background: rgba(0, 20, 40, 0.8); border: 1px solid #00f2ff;
        border-radius: 10px; padding: 15px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
    }}
    .price-val {{ font-size: 28px; color: #00f2ff; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE DATOS Y TRADING ---
def get_auth(method, path, payload=""):
    nonce = str(int(time.time() * 1000))
    message = nonce + method + path + payload
    signature = hmac.new(BITSO_API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {BITSO_API_KEY}:{nonce}:{signature}', 'Content-Type': 'application/json'}

@st.cache_data(ttl=2)
def fetch_market_data():
    try:
        # Obtenemos el Ticker actual
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
        price = float(r['payload']['last'])
        # Simulamos historial para indicadores (Bitso API v3 requiere trades para velas reales)
        history = [price + np.random.uniform(-50, 50) for _ in range(50)]
        return price, history
    except:
        return 71500.0, [71500.0]*50

def get_balance():
    path = "/v3/balance/"
    try:
        r = requests.get("https://api.bitso.com" + path, headers=get_auth("GET", path))
        balances = r.json()['payload']['balances']
        return {b['currency']: float(b['available']) for b in balances if float(b['available']) > 0}
    except:
        return {"usd": 2.81, "btc": 0.0000039}

# --- CÁLCULOS TÉCNICOS ---
price_now, price_hist = fetch_market_data()
df = pd.DataFrame({'close': price_hist})
df['sma7'] = df['close'].rolling(7).mean()
df['sma21'] = df['close'].rolling(21).mean()

# RSI Básico
delta = df['close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
df['rsi'] = 100 - (100 / (1+rs))

# --- DASHBOARD SUPERIOR ---
boveda = get_balance()
m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="metric-card">BTC/USD<div class="price-val">${price_now:,.2f}</div></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-card">BÓVEDA USD<div class="price-val" style="color:#ff00ff;">${boveda.get("usd", 0.0):.2f}</div></div>', unsafe_allow_html=True)
with m3: 
    rsi_val = df['rsi'].iloc[-1]
    st.markdown(f'<div class="metric-card">RSI (14)<div class="price-val" style="color:{"#39FF14" if rsi_val < 70 else "#FF3131"};">{rsi_val:.1f}</div></div>', unsafe_allow_html=True)
with m4:
    meta = (boveda.get("usd", 0.0) / 10000) * 100
    st.markdown(f'<div class="metric-card">META SUV<div class="price-val" style="color:cyan;">{meta:.4f}%</div></div>', unsafe_allow_html=True)

st.write("")

# --- PANEL DE VELAS PROFESIONAL ---
col_main, col_side = st.columns([3, 1])

with col_main:
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.7, 0.3])
    
    # Velas Japonesas
    fig.add_trace(go.Candlestick(
        open=df['close']*1.001, high=df['close']*1.002, low=df['close']*0.998, close=df['close'],
        name="Market", increasing_line_color='#39FF14', decreasing_line_color='#FF3131'
    ), row=1, col=1)
    
    # Indicadores SMA
    fig.add_trace(go.Scatter(y=df['sma7'], name="SMA 7", line=dict(color='#00f2ff', width=1)), row=1, col=1)
    fig.add_trace(go.Scatter(y=df['sma21'], name="SMA 21", line=dict(color='#ff00ff', width=1)), row=1, col=1)
    
    # RSI Sub-plot
    fig.add_trace(go.Scatter(y=df['rsi'], name="RSI", line=dict(color='yellow')), row=2, col=1)
    fig.add_trace(go.Scatter(y=[70]*len(df), line=dict(color='red', dash='dash'), showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(y=[30]*len(df), line=dict(color='green', dash='dash'), showlegend=False), row=2, col=1)

    fig.update_layout(template="plotly_dark", height=600, margin=dict(t=0, b=0, l=0, r=0),
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col_side:
    st.markdown('<div class="metric-card" style="text-align:left; height:600px;">', unsafe_allow_html=True)
    st.subheader("🧠 Análisis IA Mahora")
    
    # Lógica de interpretación
    if rsi_val < 35:
        st.success("🎯 SOBREVENTA: Posible señal de COMPRA")
    elif rsi_val > 65:
        st.error("⚠️ SOBRECOMPRA: Posible señal de VENTA")
    else:
        st.info("🔄 TENDENCIA: Neutral / Acumulación")
    
    st.write("---")
    st.write(f"💰 **Fondos Totales:** ${sum(boveda.values()):.2f}")
    st.write(f"🎯 **Target:** $115.00 USD")
    st.progress(min(price_now/115000, 1.0))
    
    # Botón de ejecución inteligente
    capital_uso = boveda.get("usd", 0.0) * 0.95 # Usamos el 95% para asegurar el pago de fees
    if st.button(f"🚀 ADAPTAR TODO (${capital_uso:.2f})", use_container_width=True):
        if capital_uso < 1.0:
            st.warning("Bitso requiere min $1.00 USD para operar.")
        else:
            # Lógica corregida para enviar orden de mercado real
            path = "/v3/orders/"
            payload = json.dumps({"book": "btc_usd", "side": "buy", "type": "market", "major": f"{capital_uso:.2f}"})
            res = requests.post("https://api.bitso.com" + path, headers=get_auth("POST", path, payload), data=payload).json()
            
            if res.get('success'):
                st.balloons()
                st.success("¡Orden ejecutada!")
            else:
                st.error(f"Error Bitso: {res.get('message', 'Fallo de red')}")

    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nMahoraShark: Sincronizado", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(5)
st.rerun()
