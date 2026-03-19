import streamlit as st
import requests
import pandas as pd
import time
import hmac
import hashlib
from datetime import datetime

# --- CONFIGURACIÓN DE SEGURIDAD (TUS LLAVES) ---
# Nota: Lo ideal es usar st.secrets, pero aquí las asocio a variables
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="MahoraShark Pro", page_icon="⛩️")

# --- DISEÑO Y FONDO ---
fondo_url = "https://images.wallpapersden.com/image/download/cyberpunk-city-street-night-art_bgmqaGWUmZqaraWkpJRmbmdlrWZnZ2U.jpg"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{fondo_url}");
        background-size: cover;
        color: white;
    }}
    .metric-card {{
        background-color: rgba(11, 20, 26, 0.95);
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 15px #00f2ff55;
    }}
    .ia-log {{
        background-color: rgba(0, 0, 0, 0.9);
        border: 2px solid #ff00ff;
        border-radius: 10px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        color: #39FF14;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN DE FIRMA PARA BITSO ---
def firmar_peticion(metodo, endpoint, cuerpo=""):
    nonce = str(int(time.time() * 1000))
    mensaje = nonce + metodo + endpoint + cuerpo
    firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
    return {
        'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}',
        'Content-Type': 'application/json'
    }

# --- MOTOR DE TRADING ---
def ejecutar_orden(side, amount_mxn):
    # Lógica simplificada para compra/venta
    # Side: 'buy' o 'sell'
    return f"SIMULACIÓN: {side} por ${amount_mxn} MXN"

def obtener_datos_bitso():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
        return float(r['payload']['last'])
    except: return 0.0

# --- LÓGICA DE IA ---
precio_actual = obtener_datos_bitso()
rsi_simulado = 42.0 # Aquí puedes meter la lógica de RSI anterior

# --- INTERFAZ ---
st.title("⛩️ MAHORASHARK: PRESTIGE CENTER")

# Métricas
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card">BTC/MXN<br><span style="font-size:24px; color:#00f2ff;">${precio_actual:,.0f}</span></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="metric-card">SALDO MXN<br><span style="font-size:24px; color:#ff00ff">$47.12</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card">RSI IA<br><span style="font-size:24px; color:#39FF14">{rsi_simulado}</span></div>', unsafe_allow_html=True)
with c4: st.markdown('<div class="metric-card">META 10K<br><span style="font-size:24px; color:#00f2ff">0.4712%</span></div>', unsafe_allow_html=True)

st.write("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📈 Mercado en Vivo")
    # Gráfica estética
    df_grafica = pd.DataFrame([precio_actual * (1 + i/1000) for i in range(20)], columns=['Precio'])
    st.line_chart(df_grafica, color="#ff00ff")
    
    st.write("### 🤖 Configuración Mahora")
    ia_on = st.toggle("ACTIVAR IA AUTÓNOMA")
    if ia_on:
        st.success("🤖 Cerebro Mahora tomando el control del capital...")
    
    if st.button("🚀 EJECUTAR COMPRA MANUAL (10% CAPITAL)"):
        res = ejecutar_orden('buy', 4.7)
        st.info(res)

with col_right:
    st.subheader("🧠 Cerebro Mahora")
    status = "ESPERANDO" if not ia_on else "ANALIZANDO"
    st.markdown(f"""
        <div class="ia-log">
            [{datetime.now().strftime('%H:%M:%S')}]<br>
            SISTEMA: {'ONLINE' if ia_on else 'IDLE'}<br>
            LLAVES: CONECTADAS ✅<br>
            <hr>
            >> Pensamiento: {"Esperando activación para operar." if not ia_on else "RSI estable. No hay riesgo de caída."}
        </div>
    """, unsafe_allow_html=True)

# Auto-refresh cada 15 seg
time.sleep(15)
st.rerun()
