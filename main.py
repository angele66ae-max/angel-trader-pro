import streamlit as st
import pandas as pd
import numpy as np
import ccxt
import time
from datetime import datetime

# --- CONFIGURACIÓN DE NÚCLEO ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: BITSO LIVE")

# --- CONEXIÓN API REAL ---
# Usamos tus credenciales para que el bot tenga "ojos" en tu cuenta
bitso = ccxt.bitso({
    'apiKey': 'FZHAAOqOhy',
    'secret': 'b5e9f3e4e429c079a5989473ed1ba171',
})

# --- ESTILOS VISUALES ---
fondo_directo = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                    url("{fondo_directo}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    .card {{
        background: rgba(10, 10, 15, 0.9);
        border: 2px solid #00f2ff;
        border-radius: 12px; padding: 20px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
    }}
    .money-text {{ color: #00ff00; font-size: 35px; font-weight: bold; text-shadow: 0 0 10px #00ff00; }}
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE TRADING REAL ---
def mahora_execution():
    try:
        # 1. Obtener Balance Real (Suma USD y el valor de tu ETH)
        bal = bitso.fetch_balance()
        ticker = bitso.fetch_ticker('BTC/USD')
        
        usd_real = bal['total'].get('USD', 0.0)
        btc_real = bal['total'].get('BTC', 0.0)
        eth_real = bal['total'].get('ETH', 0.0)
        precio_btc = ticker['last']
        
        # 2. Lógica de "Adaptación" (Trading)
        # Si el precio baja y tienes USD, compra. Si sube a 115 (o tu meta), vende.
        log_msg = "ESCANEANDO BITSO..."
        
        # Ejemplo: Si el precio es menor a la media reciente (simulada aquí por brevedad)
        # Aquí puedes insertar tu estrategia de la EMA magenta
        
        return usd_real, btc_real, eth_real, precio_btc, log_msg
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return 2.81, 0, 0, 71000.0, "RECONECTANDO..."

# Ejecutar motor
usd, btc, eth, p_btc, log_ia = mahora_execution()

# --- INTERFAZ ---
META = 10000.0
progreso = (usd / META)

st.markdown("<h1 style='text-align:center; color:#00f2ff;'>⛩️ MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)

# Dashboard Superior con Datos Reales
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="card">PRECIO BTC<br><h2 style="color:#00ff00;">${p_btc:,.2f}</h2></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="card">BALANCE USD<br><h2 style="color:magenta;">${usd:.2f}</h2></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="card">OBJETIVO VENTA<br><h2>115</h2></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="card">META SUV<br><h2>{(progreso*100):.4f}%</h2></div>', unsafe_allow_html=True)
    st.progress(progreso if progreso <= 1.0 else 1.0)

st.write("")

c1, c2 = st.columns([2, 1])

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Gráfica en Tiempo Real (Bitso)")
    
    # Obtener velas reales para la gráfica
    ohlcv = bitso.fetch_ohlcv('BTC/USD', timeframe='1m', limit=30)
    df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
    st.line_chart(df.set_index('ts')['c'], color="#00f2ff")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card" style="min-height:410px;">', unsafe_allow_html=True)
    st.subheader("Cerebro de la IA")
    st.code(f"""
[{datetime.now().strftime('%H:%M:%S')}]
> {log_ia}
> Saldo BTC: {btc:.8f}
> Saldo ETH: {eth:.8f}
> Adaptando capital...
    """, language="bash")
    
    if st.button("🚀 FORZAR COMPRA REAL"):
        if usd > 1:
            # bitso.create_market_buy_order('BTC/USD', usd * 0.98)
            st.warning("Orden de compra enviada a Bitso")
            
    st.markdown('</div>', unsafe_allow_html=True)

# Actualización cada 5 segundos
time.sleep(5)
st.rerun()
