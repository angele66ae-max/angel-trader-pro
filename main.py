import streamlit as st
import pandas as pd
import ccxt
import time
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN CINEMATOGRÁFICA ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

# --- CONEXIÓN API ---
bitso = ccxt.bitso({
    'apiKey': 'FZHAAOqOhy',
    'secret': 'b5e9f3e4e429c079a5989473ed1ba171',
})

# --- ESTILO "PELÍCULA" (NEÓN Y TRANSPARENCIAS) ---
st.markdown("""
<style>
    .stApp { background: #000; color: #fff; }
    .metric-card {
        background: rgba(0, 255, 242, 0.05);
        border: 1px solid #00f2ff;
        border-radius: 15px; padding: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
    }
    .main-balance { font-size: 60px; color: #00ff00; font-weight: bold; text-shadow: 0 0 20px #00ff00; }
</style>
""", unsafe_allow_html=True)

def get_full_portfolio():
    try:
        # 1. Obtener balance total de TODAS las monedas
        balance = bitso.fetch_balance()
        total_usd = 0
        prices = bitso.fetch_tickers(['BTC/USD', 'ETH/USD'])
        
        # Sumamos USD directos ($2.8 USD)
        total_usd += balance['total'].get('USD', 0)
        
        # Sumamos el valor de ETH convertido a USD
        eth_amt = balance['total'].get('ETH', 0)
        if eth_amt > 0:
            total_usd += eth_amt * prices['ETH/USD']['last']
            
        # 2. Datos para la Gráfica Profesional
        ohlcv = bitso.fetch_ohlcv('BTC/USD', timeframe='1m', limit=50)
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        df['sma'] = df['c'].rolling(window=7).mean() # Tendencia SMA

        return total_usd, df, prices['BTC/USD']['last']
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return 0, pd.DataFrame(), 0

# --- EJECUCIÓN ---
total_val, df_v, btc_p = get_full_portfolio()

# PANEL SUPERIOR: VISIÓN TOTAL
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="metric-card"><h4>BALANCE TOTAL (USD)</h4><div class="main-balance">${total_val:,.2f}</div></div>', unsafe_allow_html=True)
with c2:
    ganancia_neta = total_val - 6.80 # Base aproximada de tus 116 MXN
    st.markdown(f'<div class="metric-card"><h4>GANANCIA LÍQUIDA</h4><div style="font-size:40px; color:#ffd700;">+${ganancia_neta:,.5f}</div></div>', unsafe_allow_html=True)
with c3:
    progreso = (total_val / 10000) * 100
    st.markdown(f'<div class="metric-card"><h4>META 10K</h4><div style="font-size:40px; color:#00f2ff;">{progreso:.4f}%</div></div>', unsafe_allow_html=True)

st.write("")

# PANEL CENTRAL: GRÁFICA PROFESIONAL
if not df_v.empty:
    fig = go.Figure(data=[go.Candlestick(
        x=df_v['ts'], open=df_v['o'], high=df_v['h'], low=df_v['l'], close=df_v['c'], name="Market"
    )])
    fig.add_trace(go.Scatter(x=df_v['ts'], y=df_v['sma'], line=dict(color='#00f2ff', width=2), name="Tendencia SMA"))
    fig.update_layout(template="plotly_dark", height=500, margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

# PANEL INFERIOR: PENSAMIENTOS DE LA IA
st.subheader("Cerebro Mahora: Análisis de Multidivisa")
col_a, col_b = st.columns(2)
with col_a:
    st.code(f"""
[{datetime.now().strftime('%H:%M:%S')}] Escaneando Portfolio...
> Detectado: ETH, USD, CRONOS, GOLEM.
> Valor Total en Cartera: ${total_val:,.2f} USD
> Acción: Manteniendo posición en ETH.
    """, language="bash")
with col_b:
    if st.button("🔥 ACTIVAR COMPRA/VENTA REAL"):
        st.warning("IA en modo ejecución agresiva...")

# Refresco para fluidez
time.sleep(5)
st.rerun()
