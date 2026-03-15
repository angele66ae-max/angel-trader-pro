import streamlit as st
import pandas as pd
import numpy as np
import time
import ccxt
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: UNLEASHED")

# --- CONEXIÓN API REAL (ACTIVA) ---
bitso = ccxt.bitso({
    'apiKey': 'FZHAAOqOhy',
    'secret': 'b5e9f3e4e429c079a5989473ed1ba171',
})

# --- ESTILOS DE LUJO (DISEÑO RECUPERADO) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), url("{fondo_url}");
        background-size: cover; background-attachment: fixed;
    }}
    .main-counter {{
        background: rgba(0, 20, 20, 0.9);
        border: 3px solid #ffd700;
        border-radius: 20px; padding: 25px; text-align: center;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
        margin-bottom: 20px;
    }}
    .money-text {{
        font-family: 'Courier New', monospace;
        color: #ffd700; font-size: 65px; font-weight: bold;
        text-shadow: 0 0 20px #ffd700;
    }}
    .prestige-card {{
        background: rgba(10, 10, 15, 0.9);
        border: 1px solid #00f2ff;
        border-radius: 10px; padding: 15px; text-align: center;
    }}
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE TRADING (CON ESCUDO DE COMISIONES) ---
def mahora_engine():
    try:
        # 1. Balance Real
        bal = bitso.fetch_balance()
        usd = bal['total'].get('USD', 2.81)
        btc = bal['total'].get('BTC', 0.0)
        
        # 2. Datos de Mercado
        ohlcv = bitso.fetch_ohlcv('BTC/USD', timeframe='1m', limit=35)
        if not ohlcv: return None
        
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        df['ema'] = df['c'].ewm(span=5).mean()
        
        precio_actual = df['c'].iloc[-1]
        target_ema = df['ema'].iloc[-1]
        status = "IA ESCANEANDO..."
        
        # 3. EJECUCIÓN (CON EL 0.98 PARA EVITAR SALDO INSUFICIENTE)
        if usd > 1.0 and precio_actual < target_ema:
            # Compramos usando el 98% del saldo para cubrir comisiones de Bitso
            bitso.create_market_buy_order('BTC/USD', usd * 0.98)
            status = "🔥 COMPRA EJECUTADA"
        elif btc > 0.000005 and precio_actual > target_ema:
            bitso.create_market_sell_order('BTC/USD', btc)
            status = "⚡ VENTA EJECUTADA (PROFIT)"
            
        return usd, btc, df, status, precio_actual
    except Exception as e:
        return 2.81, 0.0, pd.DataFrame(), f"Sincronizando... {str(e)[:20]}", 71000.0

# --- RENDERIZADO DE INTERFAZ ---
engine_data = mahora_engine()

if engine_data:
    usd_val, btc_val, df_v, log_msg, p_btc = engine_data
    ganancia = usd_val - 2.81

    # SECCIÓN 1: CONTADOR DE DINERO
    st.markdown(f"""
        <div class="main-counter">
            <h3 style="color: white; margin: 0; letter-spacing: 3px;">MAHORASHARK LIQUIDITY</h3>
            <div class="money-text">${usd_val:,.6f}</div>
            <p style="color: #00ff00; font-size: 20px;">GANANCIA NETA: +${ganancia:,.6f}</p>
        </div>
    """, unsafe_allow_html=True)

    # SECCIÓN 2: GRÁFICA Y CONTROL
    st.write("")
    c1, c2 = st.columns([2.2, 1])

    with c1:
        st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
        if not df_v.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=df_v['ts'], open=df_v['o'], high=df_v['h'], low=df_v['l'], close=df_v['c'], name="BTC"
            )])
            fig.add_trace(go.Scatter(x=df_v['ts'], y=df_v['ema'], line=dict(color='#ff00ff', width=2), name="IA EMA"))
            fig.update_layout(template="plotly_dark", height=450, margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="prestige-card" style="height:485px;">', unsafe_allow_html=True)
        st.subheader("Cerebro Mahora")
        st.metric("PRECIO ACTUAL", f"${p_btc:,.2f}")
        st.metric("MI BTC", f"{btc_val:.8f}")
        st.write(f"**STATUS:** {log_msg}")
        st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nADAPTACIÓN ACTIVA\nOBJETIVO: 115", language="bash")
        if st.button("🚀 FORZAR RE-ADAPTACIÓN"):
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Refresco cada 5 segundos (Equilibrio entre velocidad y estabilidad)
time.sleep(5)
st.rerun()
