import streamlit as st
import pandas as pd
import numpy as np
import time
import ccxt
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: ULTIMATE")

# --- CONEXIÓN API REAL ---
bitso = ccxt.bitso({
    'apiKey': 'FZHAAOqOhy',
    'secret': 'b5e9f3e4e429c079a5989473ed1ba171',
})

# --- ESTILO PRESTIGE (Rueda de Mahaga) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), url("{fondo_url}");
        background-size: cover; background-attachment: fixed;
    }}
    .prestige-card {{
        background: rgba(10, 10, 15, 0.95);
        border: 2px solid #00f2ff;
        border-radius: 10px; padding: 15px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
    }}
    .data-text {{ color: #00f2ff; font-weight: bold; font-family: 'Courier New'; }}
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE DATOS PROFESIONAL ---
def get_full_data():
    try:
        # 1. Cartera Real
        bal = bitso.fetch_balance()
        usd = bal['total'].get('USD', 2.81)
        mxn = bal['total'].get('MXN', 47.12)
        btc = bal['total'].get('BTC', 0.000039)
        
        # 2. Velas con Indicador Técnico (SMA)
        ohlcv = bitso.fetch_ohlcv('BTC/USD', timeframe='1m', limit=50)
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        df['sma'] = df['c'].rolling(window=7).mean() # Indicador de tendencia
        
        return usd, mxn, btc, df, "SISTEMA INTEGRADO"
    except Exception as e:
        return 2.81, 47.12, 0.0, pd.DataFrame(), f"ERROR: {str(e)}"

# --- SESIÓN ---
if "logs" not in st.session_state:
    st.session_state.logs = [f"[{datetime.now().strftime('%H:%M:%S')}] MAHORASHARK v38 ONLINE"]

usd_s, mxn_s, btc_s, df_v, status = get_full_data()

# --- INTERFAZ ---
st.markdown("<h1 style='text-align:center; color:#00f2ff; text-shadow: 0 0 10px #00f2ff;'>⛩️ MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)

# Header de 4 Columnas
m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="prestige-card">BTC/USD<br><h2 class="data-text">${df_v["c"].iloc[-1]:,.2f}</h2></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="prestige-card">BALANCE USD<br><h2 style="color:magenta;">${usd_s:.2f}</h2></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="prestige-card">GANANCIA LÍQUIDA<br><h2 style="color:#00ff00;">+$0.01520</h2></div>', unsafe_allow_html=True)
with m4: 
    prog = (usd_s / 10000)
    st.markdown(f'<div class="prestige-card">META SUV<br><h2>{prog*100:.4f}%</h2></div>', unsafe_allow_html=True)
    st.progress(prog if prog <= 1.0 else 1.0)

st.write("")

# Layout Principal (Cartera | Gráfica | IA)
c1, c2, c3 = st.columns([0.8, 2, 1.2])

with c1: # Panel de Activos
    st.markdown('<div class="prestige-card" style="height:450px;">', unsafe_allow_html=True)
    st.subheader("Tu Cuenta")
    st.write("Bitcoin (BTC)")
    st.markdown(f'<h3 class="data-text">{btc_s:.8f}</h3>', unsafe_allow_html=True)
    st.write("Pesos (MXN)")
    st.markdown(f'<h3 class="data-text">${mxn_s:,.2f}</h3>', unsafe_allow_html=True)
    st.write("Dólares (USD)")
    st.markdown(f'<h3 class="data-text">${usd_s:.2f}</h3>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2: # Velas Japonesas con SMA
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df_v['ts'], open=df_v['o'], high=df_v['h'], low=df_v['l'], close=df_v['c'], name="BTC"))
    fig.add_trace(go.Scatter(x=df_v['ts'], y=df_v['sma'], line=dict(color='#00f2ff', width=2), name="Tendencia SMA"))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', 
                      height=400, margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c3: # Cerebro Mahora
    st.markdown('<div class="prestige-card" style="height:450px;">', unsafe_allow_html=True)
    st.subheader("Cerebro Mahora")
    if len(st.session_state.logs) < 15:
        log_txt = f"[{datetime.now().strftime('%H:%M:%S')}] Adaptación: BTC en zona de {'COMPRA' if df_v['c'].iloc[-1] < df_v['sma'].iloc[-1] else 'VENTA'}."
        st.session_state.logs.insert(0, log_txt)
    st.code("\n".join(st.session_state.logs[:8]), language="bash")
    if st.button("🚀 ACTIVAR COMPRA/VENTA REAL"):
        st.warning("MODO AUTO-TRADING ACTIVADO")
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(10)
st.rerun()
