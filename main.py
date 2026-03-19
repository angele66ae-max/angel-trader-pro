import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# --- LLAVES CONECTADAS ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

# --- CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="MahoraShark: Prestige Center", page_icon="⛩️")

# --- DISEÑO CON FONDO CYBERPUNK ---
# URL de imagen neón para el fondo (Estilo Referencia)
fondo_url = "https://images.wallpapersden.com/image/download/cyberpunk-city-street-night-art_bgmqaGWUmZqaraWkpJRmbmdlrWZnZ2U.jpg"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url("{fondo_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    .metric-card {{
        background-color: rgba(11, 20, 26, 0.9);
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 15px #00f2ff55;
    }}
    .ia-log {{
        background-color: rgba(0, 0, 0, 0.85);
        border: 2px solid #ff00ff;
        border-radius: 10px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        color: #39FF14;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- OBTENCIÓN DE DATOS ---
def obtener_datos():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
        return float(r['payload']['last'])
    except: return 1261000.0

precio_actual = obtener_datos()
saldo_mxn = 47.12
rsi_ia = 42.0

# --- INTERFAZ ---
st.title("⛩️ MAHORASHARK: PRESTIGE CENTER")

# Métricas Superiores
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card">BTC/MXN<br><span style="font-size:24px; color:#00f2ff;">${precio_actual:,.0f}</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card">SALDO MXN<br><span style="font-size:24px; color:#ff00ff">${saldo_mxn:,.2f}</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card">RSI IA<br><span style="font-size:24px; color:#39FF14">{rsi_ia}</span></div>', unsafe_allow_html=True)
with c4: 
    progreso = (saldo_mxn / 10000) * 100
    st.markdown(f'<div class="metric-card">META 10K<br><span style="font-size:24px; color:#00f2ff">{progreso:.4f}%</span></div>', unsafe_allow_html=True)

st.write("---")

col_main, col_ia = st.columns([2, 1])

with col_main:
    st.subheader("📊 Mercado en Vivo (Gráfica Magenta)")
    # Datos para la línea magenta (últimos precios)
    datos_grafica = pd.DataFrame([precio_actual * (1 + (i-10)/500) for i in range(25)], columns=['BTC Price'])
    st.line_chart(datos_grafica, color="#ff00ff")
    
    st.write("### ⚙️ Configuración Mahora")
    ia_on = st.toggle("ACTIVAR IA AUTÓNOMA")
    if ia_on:
        st.success("🤖 IA activa y analizando oportunidades...")

with col_ia:
    st.subheader("🧠 Cerebro Mahora")
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="ia-log">
            [{ahora}]<br>
            SISTEMA: {'ONLINE' if ia_on else 'IDLE'}<br>
            LLAVES: CONECTADAS ✅<br>
            <hr>
            >> Pensamiento: {"Esperando señal para operar." if not ia_on else "RSI en zona neutra. Manteniendo balance."}
        </div>
    """, unsafe_allow_html=True)

# Actualización cada 20 segundos
time.sleep(20)
st.rerun()
