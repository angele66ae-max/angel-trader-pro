import streamlit as st
import pandas as pd
import numpy as np
import time
import ccxt
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN DE PODER ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: UNLEASHED")

# --- CONEXIÓN BITSO (REAL) ---
bitso = ccxt.bitso({
    'apiKey': 'FZHAAOqOhy',
    'secret': 'b5e9f3e4e429c079a5989473ed1ba171',
})

# --- ESTILO VISUAL AGRESIVO ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url("{fondo_url}");
        background-size: cover; background-attachment: fixed;
    }}
    .main-counter {{
        background: rgba(0, 255, 242, 0.05);
        border: 3px solid #00f2ff;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 242, 255, 0.2);
    }}
    .money-text {{
        font-family: 'Courier New', monospace;
        color: #00ff00; font-size: 70px; font-weight: bold;
        text-shadow: 0 0 20px #00ff00;
    }}
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE COMPRA/VENTA REAL (ACTIVADA) ---
if usd > 0.5 and precio_actual < df['ema_fast'].iloc[-1]:
    # ELIMINA EL '#' DE LA SIGUIENTE LÍNEA PARA ACTIVAR:
    bitso.create_market_buy_order('BTC/USD', usd) 
    status = "🔥 EJECUTANDO COMPRA AGRESIVA"

elif btc > 0.00001 and precio_actual > df['ema_fast'].iloc[-1]:
    # ELIMINA EL '#' DE LA SIGUIENTE LÍNEA PARA ACTIVAR:
    bitso.create_market_sell_order('BTC/USD', btc)
    status = "⚡ EJECUTANDO VENTA (TAKE PROFIT)"
        
        # --- LÓGICA DE COMPRA/VENTA REAL ---
        # Si el precio baja de la EMA y tienes USD -> COMPRA
        # Si el precio sube de la EMA y tienes BTC -> VENTA
        status = "ESPERANDO SEÑAL..."
        
        if usd > 0.5 and precio_actual < df['ema_fast'].iloc[-1]:
            # bitso.create_market_buy_order('BTC/USD', usd)
            status = "🔥 EJECUTANDO COMPRA AGRESIVA"
        elif btc > 0.00001 and precio_actual > df['ema_fast'].iloc[-1]:
            # bitso.create_market_sell_order('BTC/USD', btc)
            status = "⚡ EJECUTANDO VENTA (TAKE PROFIT)"

        return usd, btc, df, status
    except Exception as e:
        return 2.81, 0.0, pd.DataFrame(), f"ERROR: {str(e)}"

# --- EJECUCIÓN Y RENDERIZADO ---
usd_r, btc_r, df_v, log_msg = fetch_and_trade()

# PANEL SUPERIOR: EL CONTADOR DE DINERO
st.markdown(f"""
    <div class="main-counter">
        <h2 style="color: white; letter-spacing: 5px;">MAHORASHARK LIQUIDITY</h2>
        <div class="money-text">${usd_r:,.6f}</div>
        <p style="color: #ffd700; font-size: 20px;">ESTADO: {log_msg}</p>
    </div>
""", unsafe_allow_html=True)

st.write("")

# DASHBOARD TÉCNICO
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown('<div style="background:rgba(10,10,15,0.9); padding:15px; border-radius:10px; border:1px solid #00f2ff;">', unsafe_allow_html=True)
    fig = go.Figure(data=[go.Candlestick(x=df_v['ts'], open=df_v['o'], high=df_v['h'], low=df_v['l'], close=df_v['c'])])
    fig.add_trace(go.Scatter(x=df_v['ts'], y=df_v['ema_fast'], line=dict(color='#ff00ff', width=2), name="EMA Rápida"))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', 
                      height=400, xaxis_rangeslider_visible=False, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div style="background:rgba(10,10,15,0.9); padding:15px; border-radius:10px; border:1px solid #00f2ff; height:430px;">', unsafe_allow_html=True)
    st.subheader("Cerebro Mahora")
    st.write(f"Capital en USD: ${usd_r}")
    st.write(f"Satoshi Balance: {btc_r:.8f}")
    st.code(f"""
[{datetime.now().strftime('%H:%M:%S')}] SCANNING BITSO
[{datetime.now().strftime('%H:%M:%S')}] ADAPTACIÓN: FULL
[{datetime.now().strftime('%H:%M:%S')}] TARGET: 115K
    """, language="bash")
    if st.button("🔥 FORZAR TRADE INMEDIATO"):
        st.warning("Orden enviada a Bitso...")
    st.markdown('</div>', unsafe_allow_html=True)

# Refresco ultra rápido (2 segundos) para Scalping
time.sleep(2)
st.rerun()
