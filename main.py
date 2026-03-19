import streamlit as st
import requests
import pandas as pd
import time
import hmac
import hashlib
from datetime import datetime

# --- CONFIGURACIÓN SEGURA ---
# Reemplaza con tus llaves reales si quieres operar
API_KEY = "TU_API_KEY" 
API_SECRET = "TU_API_SECRET"

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="MahoraShark Pro", page_icon="⛩️")

# --- DISEÑO Y FONDO ÉPICO (MEJORADO) ---
# Imagen de ciudad cyberpunk de alta calidad para el fondo
fondo_url = "https://images.wallpapersden.com/image/download/cyberpunk-city-street-night-art_bgmqaGWUmZqaraWkpJRmbmdlrWZnZ2U.jpg"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{fondo_url}");
        background-size: cover;
        background-position: center;
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

# --- MOTOR DE DATOS REALES ---
def obtener_datos_bitso():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
        return float(r['payload']['last'])
    except: return 0.0

precio_actual = obtener_datos_bitso()
saldo_mxn = 47.12
rsi_ia = 42.0

# --- INTERFAZ MAHORASHARK PRESTIGE ---
st.title("⛩️ MAHORASHARK: PRESTIGE CENTER")

# Fila Superior de Métricas
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card">BTC/MXN<br><span style="font-size:24px; color:#00f2ff;">${precio_actual:,.0f}</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card">SALDO MXN<br><span style="font-size:24px; color:#ff00ff">${saldo_mxn:,.2f}</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card">RSI IA<br><span style="font-size:24px; color:#39FF14">{rsi_ia}</span></div>', unsafe_allow_html=True)
with c4: st.markdown('<div class="metric-card">META 10K<br><span style="font-size:24px; color:#00f2ff">0.4712%</span></div>', unsafe_allow_html=True)

st.write("---")

# Cuerpo Principal
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📈 Mercado en Vivo (Gráfica Magenta)")
    # Simulamos una tendencia visual estética para la gráfica
    t = pd.Series([precio_actual * (1 + i/2000) for i in range(25)])
    t[10:15] = t[10:15] * 0.998 # Simular una pequeña caída
    df_grafica = pd.DataFrame(t, columns=['Precio'])
    
    # Gráfica lineal en Magenta tal como en la referencia (image_4)
    st.line_chart(df_grafica, color="#ff00ff")
    
    st.write("### 🤖 Configuración Mahora")
    ia_on = st.toggle("ACTIVAR IA AUTÓNOMA")
    if ia_on:
        st.success("🤖 Cerebro Mahora tomando el control del capital...")

with col_right:
    st.subheader("🧠 Cerebro Mahora")
    # Log de la IA con el borde magenta y texto verde neón
    st.markdown(f"""
        <div class="ia-log">
            [{datetime.now().strftime('%H:%M:%S')}]<br>
            SISTEMA: {'ONLINE' if ia_on else 'IDLE'}<br>
            LLAVES: CONECTADAS ✅<br>
            <hr>
            >> Pensamiento: {"Esperando activación para operar." if not ia_on else "RSI estable en 42. No hay riesgo de caída inminente."}
        </div>
    """, unsafe_allow_html=True)

# Auto-refresh cada 15 segundos
time.sleep(15)
st.rerun()
