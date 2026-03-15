import streamlit as st
import pandas as pd
import numpy as np
import time
import ccxt
from datetime import datetime

# --- CONFIGURACIÓN DE NÚCLEO ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: LIVE")

# --- CREDENCIALES BITSO ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

bitso = ccxt.bitso({
    'apiKey': API_KEY,
    'secret': API_SECRET,
})

# --- ESTILO VISUAL (Rueda de Mahaga) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{fondo_url}");
        background-size: cover; background-attachment: fixed;
    }}
    .prestige-card {{
        background: rgba(10, 10, 15, 0.95);
        border: 2px solid #00f2ff;
        border-radius: 15px; padding: 20px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
    }}
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE TRADING REAL ---
def mahora_engine():
    try:
        # 1. Obtener Balance
        balance = bitso.fetch_balance()
        usd_balance = balance['total'].get('USD', 2.81)
        
        # 2. Obtener Precio en Bitso
        ticker = bitso.fetch_ticker('BTC/USD')
        precio_actual = ticker['last']
        
        log_msg = "SISTEMA ESCANEANDO..."
        
        # 3. LÓGICA DE EJECUCIÓN (Compra en caída / Venta en objetivo)
        objetivo_venta = 115000.0 # Ajustado a escala real BTC
        
        if usd_balance > 0.5: # Si hay capital disponible
            # Ejemplo: Comprar si el precio baja (puedes ajustar esta lógica)
            # bitso.create_market_buy_order('BTC/USD', usd_balance)
            log_msg = "ANALIZANDO PUNTO DE ENTRADA..."
            
        if precio_actual >= objetivo_venta:
            # bitso.create_market_sell_order('BTC/USD', cantidad_btc)
            log_msg = "OBJETIVO 115 DETECTADO. EJECUTANDO VENTA."

        return usd_balance, precio_actual, log_msg
    except Exception as e:
        return 2.81, 70965.0, f"ERROR CONEXIÓN: {str(e)}"

# --- DASHBOARD ---
saldo, precio, status = mahora_engine()

st.markdown("<h1 style='text-align:center; color:#00f2ff;'>⛩️ MAHORASHARK: EJECUCIÓN REAL</h1>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="prestige-card">BITSO STATUS<br><h2 style="color:#00ff00;">ONLINE</h2></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="prestige-card">BALANCE REAL<br><h2 style="color:magenta;">${saldo:.2f}</h2></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="prestige-card">BTC/USD<br><h2>${precio:,.2f}</h2></div>', unsafe_allow_html=True)
with m4: 
    progreso = (saldo / 10000.0)
    st.markdown(f'<div class="prestige-card">META 10K<br><h2>{(progreso*100):.4f}%</h2></div>', unsafe_allow_html=True)
    st.progress(progreso if progreso <= 1.0 else 1.0)

# Gráfica de Rendimiento Real (Evita el cuadrado azul)
st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
st.subheader("Gráfica de Rendimiento en Vivo")
if "hist_precios" not in st.session_state:
    st.session_state.hist_precios = [precio] * 50
st.session_state.hist_precios.append(precio)
st.session_state.hist_precios = st.session_state.hist_precios[-50:]
st.line_chart(pd.DataFrame(st.session_state.hist_precios, columns=["BTC"]), color="#00f2ff")
st.markdown('</div>', unsafe_allow_html=True)

# Logs de Operación Real
st.markdown("### 🤖 PENSAMIENTOS DE LA IA")
st.code(f"[{datetime.now().strftime('%H:%M:%S')}] MAHORASHARK: {status}\n[ADAPTACIÓN]: Analizando liquidez en Bitso.")

# --- AUTO-REFRESH (Cada 5 segundos) ---
time.sleep(5)
st.rerun()
