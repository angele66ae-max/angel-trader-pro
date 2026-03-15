import streamlit as st
import pandas as pd
import numpy as np
import time
import ccxt
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: WEALTH")

# --- CONEXIÓN API REAL ---
bitso = ccxt.bitso({
    'apiKey': 'FZHAAOqOhy',
    'secret': 'b5e9f3e4e429c079a5989473ed1ba171',
})

# --- ESTILOS PRESTIGE ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{fondo_url}");
        background-size: cover; background-attachment: fixed;
    }}
    .money-card {{
        background: rgba(0, 20, 20, 0.9);
        border: 2px solid #ffd700;
        border-radius: 15px; padding: 20px; text-align: center;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.3);
        margin-bottom: 20px;
    }}
    .prestige-card {{
        background: rgba(10, 10, 15, 0.9);
        border: 1px solid #00f2ff;
        border-radius: 10px; padding: 15px; text-align: center;
    }}
    .counter-value {{
        font-family: 'Courier New', monospace;
        color: #ffd700; font-size: 50px; font-weight: bold;
        text-shadow: 0 0 15px #ffd700;
    }}
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE DATOS ---
def get_wealth_data():
    try:
        # Cartera real
        bal = bitso.fetch_balance()
        usd = bal['total'].get('USD', 2.81)
        mxn = bal['total'].get('MXN', 47.12)
        btc = bal['total'].get('BTC', 0.000039)
        
        # Velas y SMA
        ohlcv = bitso.fetch_ohlcv('BTC/USD', timeframe='1m', limit=30)
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        df['sma'] = df['c'].rolling(window=7).mean()
        
        return usd, mxn, btc, df
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return 2.81, 47.12, 0.0, pd.DataFrame()

# --- EJECUCIÓN ---
usd_val, mxn_val, btc_val, df_v = get_wealth_data()
ganancia = usd_val - 2.81 # Calculado sobre tu base real

# --- INTERFAZ ---
st.markdown("<h1 style='text-align:center; color:#00f2ff;'>⛩️ MAHORASHARK: WEALTH CENTER</h1>", unsafe_allow_html=True)

# 1. EL CONTADOR DE DINERO (IMPACTO TOTAL)
st.markdown(f"""
    <div class="money-card">
        <p style="color: white; font-size: 18px; letter-spacing: 2px;">VALOR TOTAL DE LA CUENTA (USD)</p>
        <div class="counter-value">${usd_val:,.6f}</div>
        <p style="color: #00ff00; font-size: 20px;">↑ GANANCIA NETA: +${ganancia:,.6f}</p>
    </div>
""", unsafe_allow_html=True)

# 2. INDICADORES SUPERIORES
m1, m2, m3 = st.columns(3)
with m1: st.markdown(f'<div class="prestige-card">BTC PRICE<br><h2 style="color:#00f2ff;">${df_v["c"].iloc[-1]:,.2f}</h2></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="prestige-card">META SUV<br><h2>$10,000.00</h2></div>', unsafe_allow_html=True)
with m3: 
    prog = (usd_val / 10000)
    st.markdown(f'<div class="prestige-card">PROGRESO<br><h2>{prog*100:.5f}%</h2></div>', unsafe_allow_html=True)

st.write("")

# 3. CUERPO TÉCNICO (Velas | Cuenta | IA)
c1, c2, c3 = st.columns([2, 0.8, 1])

with c1: # Velas Japonesas
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    fig = go.Figure(data=[go.Candlestick(x=df_v['ts'], open=df_v['o'], high=df_v['h'], low=df_v['l'], close=df_v['c'], name="BTC")])
    fig.add_trace(go.Scatter(x=df_v['ts'], y=df_v['sma'], line=dict(color='#00f2ff', width=2), name="Tendencia SMA"))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', 
                      height=400, margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2: # Activos Reales
    st.markdown('<div class="prestige-card" style="height:440px;">', unsafe_allow_html=True)
    st.subheader("Holdings")
    st.write("BTC")
    st.code(f"{btc_val:.8f}")
    st.write("MXN")
    st.code(f"${mxn_val:,.2f}")
    st.write("USD")
    st.code(f"${usd_val:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

with c3: # Cerebro Mahora
    st.markdown('<div class="prestige-card" style="height:440px;">', unsafe_allow_html=True)
    st.subheader("Log de IA")
    st.code(f"""
[{datetime.now().strftime('%H:%M:%S')}] Escaneando Bitso...
[{datetime.now().strftime('%H:%M:%S')}] Capital: ${usd_val}
[{datetime.now().strftime('%H:%M:%S')}] Objetivo 115 activo.
    """, language="bash")
    if st.button("🚀 FORZAR EJECUCIÓN"):
        st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

# Refresco rápido para el contador
time.sleep(5)
st.rerun()
