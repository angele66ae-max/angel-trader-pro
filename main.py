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

# --- ESTILO VISUAL PRESTIGE ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: white; }
    .main-counter {
        background: rgba(0, 255, 100, 0.1);
        border: 2px solid #00ff00;
        border-radius: 15px; padding: 25px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
    }
    .money-text { font-family: 'monospace'; color: #00ff00; font-size: 60px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE TRADING REAL ---
def mahora_engine():
    try:
        # 1. Obtener balance real
        bal = bitso.fetch_balance()
        usd = bal['total'].get('USD', 2.81)
        btc = bal['total'].get('BTC', 0.0)
        
        # 2. Obtener mercado (Velas rápidas de 1m)
        ohlcv = bitso.fetch_ohlcv('BTC/USD', timeframe='1m', limit=35)
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        
        # 3. EMA Rápida (Línea Magenta)
        df['ema_fast'] = df['c'].ewm(span=5).mean()
        precio_actual = df['c'].iloc[-1]
        target_ema = df['ema_fast'].iloc[-1]
        
        status = "Buscando entrada..."
        
        # --- EJECUCIÓN AUTOMÁTICA (DESBLOQUEADA) ---
        # Si el precio baja de la EMA y hay USD -> COMPRAMOS
        if usd > 1.0 and precio_actual < target_ema:
            bitso.create_market_buy_order('BTC/USD', usd)
            status = "🔥 COMPRA REALIZADA"
        
        # Si el precio sube de la EMA y hay BTC -> VENDEMOS
        elif btc > 0.00001 and precio_actual > target_ema:
            bitso.create_market_sell_order('BTC/USD', btc)
            status = "⚡ VENTA REALIZADA (PROFIT)"

        return usd, btc, df, status, precio_actual
    except Exception as e:
        return 2.81, 0.0, pd.DataFrame(), f"Esperando API...", 71000.0

# --- INTERFAZ ---
usd_r, btc_r, df_v, log_msg, p_act = mahora_engine()

st.markdown(f"""
    <div class="main-counter">
        <h3 style="margin:0;">MAHORASHARK LIQUIDITY</h3>
        <div class="money-text">${usd_r:,.6f}</div>
        <p style="color: #00f2ff; font-size: 18px;">ESTADO IA: {log_msg}</p>
    </div>
""", unsafe_allow_html=True)

st.write("")
col1, col2 = st.columns([2, 1])

with col1:
    # Gráfica de Velas con EMA
    fig = go.Figure(data=[go.Candlestick(x=df_v['ts'], open=df_v['o'], high=df_v['h'], low=df_v['l'], close=df_v['c'])])
    fig.add_trace(go.Scatter(x=df_v['ts'], y=df_v['ema_fast'], line=dict(color='#ff00ff', width=2), name="EMA Mahora"))
    fig.update_layout(template="plotly_dark", height=450, margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(f'<div style="border:1px solid #333; padding:15px; border-radius:10px;">', unsafe_allow_html=True)
    st.subheader("Cerebro Mahora")
    st.metric("BTC PRICE", f"${p_act:,.2f}")
    st.metric("SATOSHIS", f"{btc_r:.8f}")
    st.code(f"[{datetime.now().strftime('%H:%M:%S')}] ADAPTANDO AL MERCADO...")
    st.markdown('</div>', unsafe_allow_html=True)

# Loop de 3 segundos para modo scalping
time.sleep(3)
st.rerun()
