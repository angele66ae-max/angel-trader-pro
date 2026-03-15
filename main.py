import streamlit as st
import pandas as pd
import ccxt
import time
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN DE TERMINAL ---
st.set_page_config(layout="wide", page_title="MAHORA: AGGRESSIVE")

# --- CONEXIÓN API ---
bitso = ccxt.bitso({
    'apiKey': 'FZHAAOqOhy',
    'secret': 'b5e9f3e4e429c079a5989473ed1ba171',
})

# --- ESTILO DARK ---
st.markdown("""
<style>
    .stApp { background-color: #030303; color: #fff; }
    .card {
        background: rgba(20, 20, 25, 0.95);
        border: 1px solid #00f2ff;
        border-radius: 8px; padding: 15px; text-align: center;
    }
    .money { font-size: 45px; color: #00ff00; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def trade_logic():
    try:
        # 1. Datos Reales de Cartera
        bal = bitso.fetch_balance()
        usd = bal['total'].get('USD', 0.0)
        btc = bal['total'].get('BTC', 0.0)
        
        # 2. Análisis Técnico (Velas de 1 minuto)
        ohlcv = bitso.fetch_ohlcv('BTC/USD', timeframe='1m', limit=30)
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        
        # He acortado la EMA a 5 para que la IA reaccione MUCHO más rápido
        df['ema_fast'] = df['c'].ewm(span=5).mean()
        
        precio = df['c'].iloc[-1]
        ema = df['ema_fast'].iloc[-1]
        
        status = "BUSCANDO ENTRADA..."
        
        # 3. EJECUCIÓN REAL (SIN MIEDO)
        # Compramos si el precio toca o baja ligeramente de la EMA rápida
        if usd > 0.50 and precio <= (ema * 1.0005): 
            bitso.create_market_buy_order('BTC/USD', usd * 0.98)
            status = "🔥 COMPRA REAL EJECUTADA"
            
        # Vendemos apenas haya un pequeño salto arriba de la EMA
        elif btc > 0.000001 and precio > ema:
            bitso.create_market_sell_order('BTC/USD', btc)
            status = "⚡ VENTA REAL (PROFIT)"

        return usd, btc, df, status, precio
    except Exception as e:
        return 0, 0, pd.DataFrame(), f"Error: {str(e)[:30]}", 0

# --- INTERFAZ ---
u_real, b_real, df_data, log, p_now = trade_logic()

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="card"><small>DÓLARES (USD)</small><div class="money">${u_real:,.2f}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="card"><small>ACCIÓN IA</small><div style="font-size:20px; color:#ffd700;">{log}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="card"><small>BTC ACTUAL</small><div style="font-size:30px; color:#00f2ff;">${p_now:,.2f}</div></div>', unsafe_allow_html=True)

st.write("")
col_a, col_b = st.columns([2.5, 1])

with col_a:
    if not df_data.empty:
        fig = go.Figure(data=[go.Candlestick(x=df_data['ts'], open=df_data['o'], high=df_data['h'], low=df_data['l'], close=df_data['c'])])
        fig.add_trace(go.Scatter(x=df_data['ts'], y=df_data['ema_fast'], line=dict(color='#ff00ff', width=2), name="Cerebro"))
        fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.markdown('<div class="card" style="text-align:left; height:400px;">', unsafe_allow_html=True)
    st.subheader("Estado Real")
    st.write(f"**Bitcoin:** `{b_real:.8f}`")
    st.write(f"**Time:** {datetime.now().strftime('%H:%M:%S')}")
    st.divider()
    st.info("Modo: Agresivo (EMA 5). El bot operará ante el más mínimo movimiento.")
    if st.button("FORZAR OPERACIÓN"):
        st.write("Sincronizando con Bitso...")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Refresco cada 3 segundos para no perder ni un "tick" del mercado
time.sleep(3)
st.rerun()
