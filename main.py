import streamlit as st
import pandas as pd
import ccxt
import time
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN DE TERMINAL ---
st.set_page_config(layout="wide", page_title="MAHORA: REAL CORE")

# --- CONEXIÓN API (BITSO) ---
bitso = ccxt.bitso({
    'apiKey': 'FZHAAOqOhy',
    'secret': 'b5e9f3e4e429c079a5989473ed1ba171',
})

# --- ESTILO PROFESIONAL ESTÁTICO ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    .status-card {
        background: rgba(10, 20, 30, 0.9);
        border: 2px solid #00f2ff;
        border-radius: 10px; padding: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
    }
    .price-text { color: #00ff00; font-size: 48px; font-weight: bold; text-shadow: 0 0 10px #00ff00; }
</style>
""", unsafe_allow_html=True)

def execute_mahora_logic():
    try:
        # 1. Captura de Balance Real
        balance = bitso.fetch_balance()
        usd_balance = balance['total'].get('USD', 0.0)
        btc_balance = balance['total'].get('BTC', 0.0)
        eth_balance = balance['total'].get('ETH', 0.0)
        
        # 2. Análisis de Mercado (BTC/USD)
        ohlcv = bitso.fetch_ohlcv('BTC/USD', timeframe='1m', limit=50)
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        df['ema'] = df['c'].ewm(span=7).mean()
        
        precio_actual = df['c'].iloc[-1]
        indicador_ema = df['ema'].iloc[-1]
        
        # 3. LÓGICA DE TRADING REAL (SIN DINERO DE PAPEL)
        log_action = "IA ESCANEANDO MERCADO..."
        
        # COMPRA: Si el precio cae por debajo de la EMA y tenemos más de $1 USD
        if usd_balance > 1.0 and precio_actual < indicador_ema:
            # Usamos el 98% para cubrir comisiones de Bitso
            bitso.create_market_buy_order('BTC/USD', usd_balance * 0.98)
            log_action = "🔥 ORDEN DE COMPRA EJECUTADA"
            
        # VENTA: Si el precio sube por encima de la EMA y tenemos BTC
        elif btc_balance > 0.000001 and precio_actual > indicador_ema:
            bitso.create_market_sell_order('BTC/USD', btc_balance)
            log_action = "⚡ ORDEN DE VENTA (PROFIT) ENVIADA"

        return usd_balance, btc_balance, eth_balance, df, log_action, precio_actual
    except Exception as e:
        return 0, 0, 0, pd.DataFrame(), f"Error: {str(e)}", 0

# --- DESPLIEGUE ---
usd_r, btc_r, eth_r, df_m, status, p_btc = execute_mahora_logic()

# HEADER DE ESTADO
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="status-card"><small>SALDO USD REAL</small><div class="price-text">${usd_r:,.2f}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="status-card"><small>ESTADO DE IA</small><div style="font-size:24px; color:#ffd700; margin-top:10px;">{status}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="status-card"><small>PRECIO BTC</small><div style="font-size:32px; color:#00f2ff; margin-top:10px;">${p_btc:,.2f}</div></div>', unsafe_allow_html=True)

st.write("")
col_grafica, col_info = st.columns([2.5, 1])

with col_grafica:
    if not df_m.empty:
        fig = go.Figure(data=[go.Candlestick(x=df_m['ts'], open=df_m['o'], high=df_m['h'], low=df_m['l'], close=df_m['c'], name="Market")])
        fig.add_trace(go.Scatter(x=df_m['ts'], y=df_m['ema'], line=dict(color='#ff00ff', width=2), name="IA Core"))
        fig.update_layout(template="plotly_dark", height=450, margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

with col_info:
    st.markdown('<div class="status-card" style="text-align:left;">', unsafe_allow_html=True)
    st.subheader("Bóveda Real")
    st.write(f"**Ether (ETH):** `{eth_r:.7f}`")
    st.write(f"**Bitcoin (BTC):** `{btc_r:.8f}`")
    st.divider()
    st.code(f"SINC: {datetime.now().strftime('%H:%M:%S')}\nMODO: EJECUCIÓN REAL")
    if st.button("🔄 ACTUALIZAR"): st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Refresco cada 5 segundos para máxima precisión
time.sleep(5)
st.rerun()
