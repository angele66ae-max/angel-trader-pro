import streamlit as st
import pandas as pd
import numpy as np
import time
import ccxt
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN DE NÚCLEO ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: BITSO PRESTIGE")

# --- CONEXIÓN REAL A BITSO ---
bitso = ccxt.bitso({
    'apiKey': 'FZHAAOqOhy',
    'secret': 'b5e9f3e4e429c079a5989473ed1ba171',
})

# --- DISEÑO VISUAL (Rueda de Mahaga) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{fondo_url}");
        background-size: cover; background-attachment: fixed;
    }}
    .prestige-card {{
        background: rgba(10, 10, 15, 0.92);
        border: 2px solid #00f2ff;
        border-radius: 12px; padding: 20px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
    }}
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE DATOS EN VIVO ---
def get_live_data():
    try:
        balance_info = bitso.fetch_balance()
        usd_balance = balance_info['total'].get('USD', balance_info['total'].get('MXN', 2.81))
        
        # Obtenemos OHLCV (Velas: Open, High, Low, Close, Volume)
        ohlcv = bitso.fetch_ohlcv('BTC/USD', timeframe='1m', limit=30)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        return usd_balance, df, "SISTEMA LIVE"
    except Exception as e:
        return 2.81, pd.DataFrame(), f"ERROR: {str(e)}"

# --- LÓGICA DE SESIÓN ---
if "log_ia_hist" not in st.session_state:
    st.session_state.log_ia_hist = [f"[{datetime.now().strftime('%H:%M:%S')}] MAHORA ADAPTATION START..."]

saldo, df_velas, status = get_live_data()
btc_p = df_velas['close'].iloc[-1] if not df_velas.empty else 70000.0

# --- INTERFAZ ---
st.markdown("<h1 style='text-align:center; color:#00f2ff;'>⛩️ MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="prestige-card">ESTADO<br><h2 style="color:#00ff00;">GENERANDO</h2></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="prestige-card">BALANCE REAL<br><h2 style="color:magenta;">${saldo:.2f}</h2></div>', unsafe_allow_html=True)
with m3: st.markdown('<div class="prestige-card">META SUV<br><h2>$10,000.00</h2></div>', unsafe_allow_html=True)
with m4: 
    progreso = (saldo / 10000.0)
    st.markdown(f'<div class="prestige-card">PROGRESO<br><h2>{(progreso*100):.4f}%</h2></div>', unsafe_allow_html=True)
    st.progress(progreso if progreso <= 1.0 else 1.0)

st.write("")

c1, c2 = st.columns([2, 1])

with c1:
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    st.subheader("Análisis de Velas Japonesas (BTC/USD)")
    
    if not df_velas.empty:
        fig = go.Figure(data=[go.Candlestick(
            x=df_velas['timestamp'],
            open=df_velas['open'],
            high=df_velas['high'],
            low=df_velas['low'],
            close=df_velas['close'],
            increasing_line_color='#00ff00', decreasing_line_color='#ff0000'
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='white', margin=dict(l=0, r=0, t=0, b=0),
            xaxis_rangeslider_visible=False, height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Cargando datos de Bitso...")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="prestige-card" style="min-height:430px;">', unsafe_allow_html=True)
    st.subheader("Pensamientos de la IA")
    
    if len(st.session_state.log_ia_hist) < 15:
        frases = [
            f"Analizando patrones de velas...",
            f"Escaneando liquidez para proteger ${saldo}.",
            f"Objetivo 115 en mira táctica.",
            f"Adaptación Mahora al {np.random.randint(98, 100)}%."
        ]
        st.session_state.log_ia_hist.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] {np.random.choice(frases)}")
    
    st.code("\n".join(st.session_state.log_ia_hist[:8]), language="bash")
    
    if st.button("🚀 ACTIVAR OPERACIÓN REAL"):
        st.error("MAHORASHARK TOMANDO CONTROL...")
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(10) # 10 segundos para no saturar la API de Bitso
st.rerun()
