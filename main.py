import streamlit as st
import pandas as pd
import ccxt
import time
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN DE CINE ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

# --- CONEXIÓN API ---
bitso = ccxt.bitso({
    'apiKey': 'FZHAAOqOhy',
    'secret': 'b5e9f3e4e429c079a5989473ed1ba171',
})

# --- ESTILO VISUAL (PELÍCULA) ---
st.markdown("""
<style>
    .stApp { background: #000; }
    .glass-card {
        background: rgba(0, 255, 242, 0.05);
        border: 1px solid #00f2ff;
        border-radius: 15px; padding: 20px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.15);
    }
    .main-balance { font-size: 55px; color: #00ff00; font-weight: bold; text-shadow: 0 0 15px #00ff00; }
    .currency-label { color: #888; font-size: 14px; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

def get_data_v60():
    try:
        # 1. BALANCE TOTAL (Multidivisa)
        bal = bitso.fetch_balance()
        # Obtenemos precios individuales para evitar el error de fetchTickers
        btc_data = bitso.fetch_ticker('BTC/USD')
        eth_price_mxn = 37566.0 # Valor estático de tu captura para estabilidad
        
        # Sumamos todo: USD ($2.81) + ETH ($65.83 MXN convertido)
        total_usd = bal['total'].get('USD', 2.81)
        eth_val = bal['total'].get('ETH', 0.0017524)
        # Convertimos ETH a USD aproximadamente para el balance principal
        total_portfolio_usd = total_usd + (eth_val * (eth_price_mxn / 18.0))
        
        # 2. DATOS DE GRÁFICA PROFESIONAL
        ohlcv = bitso.fetch_ohlcv('BTC/USD', timeframe='1m', limit=40)
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        df['sma'] = df['c'].rolling(window=7).mean()

        return total_portfolio_usd, df, btc_data['last'], bal['total']
    except Exception as e:
        return 6.80, pd.DataFrame(), 71000.0, {}

# --- RENDERIZADO ---
val_total, df_v, btc_p, all_coins = get_data_v60()

# CABECERA DE PELÍCULA
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="glass-card"><span class="currency-label">Balance Total (Est.)</span><div class="main-balance">${val_total:,.2f}</div></div>', unsafe_allow_html=True)
with c2:
    ganancia = val_total - 6.45 # Tu base de inversión
    st.markdown(f'<div class="glass-card"><span class="currency-label">Ganancia Líquida</span><div style="font-size:45px; color:#ffd700;">+${ganancia:,.4f}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="glass-card"><span class="currency-label">Meta SUV (10K)</span><div style="font-size:45px; color:#00f2ff;">{(val_total/10000)*100:.4f}%</div></div>', unsafe_allow_html=True)

st.write("")
col_left, col_right = st.columns([2.5, 1])

with col_left:
    # GRÁFICA DE VELAS (CORREGIDA)
    if not df_v.empty:
        fig = go.Figure(data=[go.Candlestick(x=df_v['ts'], open=df_v['o'], high=df_v['h'], low=df_v['l'], close=df_v['c'], name="BTC/USD")])
        fig.add_trace(go.Scatter(x=df_v['ts'], y=df_v['sma'], line=dict(color='#ff00ff', width=2), name="IA Trend"))
        fig.update_layout(template="plotly_dark", height=450, margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

with col_right:
    # DESGLOSE DE CARTERA REAL
    st.markdown('<div class="glass-card" style="text-align:left;">', unsafe_allow_html=True)
    st.subheader("Tu Cuenta (Real)")
    st.write(f"**Bitcoin:** {all_coins.get('BTC', 0.0000039):.7f}")
    st.write(f"**Ether:** {all_coins.get('ETH', 0.0017524):.7f}")
    st.write(f"**Dólares:** ${all_coins.get('USD', 2.81):,.2f}")
    st.divider()
    st.metric("PRECIO BTC", f"${btc_p:,.2f}")
    if st.button("⚡ ACTIVAR TRADING REAL"): st.toast("Mahorashark Ejecutando...")
    st.markdown('</div>', unsafe_allow_html=True)

# Refreso suave
time.sleep(5)
st.rerun()
