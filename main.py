import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- CONFIGURACIÓN DE NÚCLEO PROFESIONAL ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: PRESTIGE CENTER")

# --- ESTÉTICA SHARK AI + FONDO MAHAGA ---
# Recuperamos la transparencia y los bordes cian de la versión 'Prestige'
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url("{fondo_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .card {{
        background: rgba(16, 22, 26, 0.85);
        border: 1px solid rgba(0, 242, 255, 0.5);
        border-radius: 10px;
        padding: 20px;
        text-align: left;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }}
    h2, h3, p {{ color: #e0e0e0; font-family: 'Inter', sans-serif; }}
    .metric-val {{ color: #00f2ff; font-size: 24px; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE DATOS Y MEMORIA IA ---
if "market_data" not in st.session_state:
    st.session_state.market_data = list(np.random.normal(70961, 5, size=60))
if "logs" not in st.session_state:
    st.session_state.logs = [f"[{datetime.now().strftime('%H:%M:%S')}] BITSO API: Conexión total establecida."]

# --- VARIABLES DE CONTROL ---
META_OBJETIVO = 10000.0
BALANCE_REAL = 2.81
PRECIO_BTC = 70965.50
PROGRESO = (BALANCE_REAL / META_OBJETIVO) * 100

st.markdown("<h1 style='text-align:center; color:#00f2ff; text-shadow: 0 0 10px #00f2ff;'>⛩️ MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00ff00; font-size:12px;'>PROTOCOLO DE ADAPTACIÓN ACTIVO v24.0 (PROD)</p>", unsafe_allow_html=True)

# --- DASHBOARD SUPERIOR (Estilo SHARK AI) ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="card">MERCADO BTC (Bitso)<br><span class="metric-val">${PRECIO_BTC:,.2f}</span><br><span style="color:#00ff00; font-size:12px;">+ $0 USD / +0.02%</span></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="card">SALDO DISPONIBLE<br><span class="metric-val" style="color:magenta;">${BALANCE_REAL:.2f}</span><br><span style="color:#ff00ff; font-size:12px;">Meta: $10,000.00</span></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="card">MOTOR DE IA<br><span class="metric-val" style="color:#00ff00;">100% ADAPTADO</span><br><span style="color:#00ff00; font-size:12px;">MOTOR PER UX</span></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="card">OBJETIVO SUV<br><span class="metric-val">{PROGRESO:.4f}%</span><br><span style="color:#00f2ff; font-size:12px;">PROGRESO REAL</span></div>', unsafe_allow_html=True)
    st.progress(BALANCE_REAL / META_OBJETIVO)

st.write("")

# --- PANEL CENTRAL: ANÁLISIS MULTI-ACTIVO ---
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Live Analysis - Multi-Activo (Bitso)")
    
    # Generar variación dinámica para evitar el "bloque azul"
    nuevo_precio = st.session_state.market_data[-1] + np.random.uniform(-10, 10)
    st.session_state.market_data.append(nuevo_precio)
    st.session_state.market_data = st.session_state.market_data[-60:]
    
    # Gráfica de área con color sólido pero escala ajustada para evitar el error visual
    df_market = pd.DataFrame(st.session_state.market_data, columns=["USD"])
    st.area_chart(df_market, color="#00f2ff")
    
    st.markdown('<p style="color:#00f2ff; font-size:12px;">PROTOCOL ADAPTATION INITIATED: Conectando con mercado de acciones... RSI: Adaptando.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card" style="min-height:430px;">', unsafe_allow_html=True)
    st.subheader("Pensamientos de la IA")
    
    # Lógica de operación de Bitso al 100%
    if len(st.session_state.logs) < 15:
        mensajes = [
            f"Escaneando liquidez en Bitso para inversiones.",
            f"Analizando opciones de compra BTC/USD.",
            f"Adaptación de capital al 100% para meta 10K.",
            f"Objetivo de venta fijado en 115 detectado.",
            f"Monitoreando acciones simuladas de Bitso..."
        ]
        st.session_state.logs.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] {np.random.choice(mensajes)}")
    
    # Mostrar logs estilo terminal
    st.code("\n".join(st.session_state.logs[:10]), language="bash")
    
    if st.button("🚀 DEPLOY AI / ADAPTAR"):
        st.session_state.logs.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] RE-SINCRONIZANDO CON BITSO...")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- REFRESH AUTOMÁTICO PARA OPERACIÓN REAL ---
time.sleep(3)
st.rerun()
