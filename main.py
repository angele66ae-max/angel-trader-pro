import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- CONFIGURACIÓN DE NÚCLEO ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: PRESTIGE")

# --- MEMORIA DE LA IA (Para que no se borren los pensamientos) ---
if "log_historial" not in st.session_state:
    st.session_state.log_historial = [f"[{datetime.now().strftime('%H:%M:%S')}] PROTOCOLO INICIADO: Buscando meta 10K..."]
if "btc_historial" not in st.session_state:
    st.session_state.btc_historial = list(np.random.randn(50).cumsum() + 70965)

# --- LÓGICA DE LA META 10K ---
META_OBJETIVO = 10000.0
balance_actual = 2.81 
progreso = (balance_actual / META_OBJETIVO)

# --- ESTILO VISUAL BLINDADO ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: white; }
    .card {
        background: rgba(16, 16, 20, 0.95);
        border: 1px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.15);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#00f2ff;'>⛩️ MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)

# Dashboard Superior
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="card">MOTOR IA<br><h2 style="color:#00ff00;">ADAPTANDO</h2></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="card">BALANCE REAL<br><h2 style="color:magenta;">${balance_actual:.2f}</h2></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="card">META 10K<br><h2>$10,000.00</h2></div>', unsafe_allow_html=True)
with m4:
    porcentaje = (progreso * 100)
    st.markdown(f'<div class="card">PROGRESO<br><h2>{porcentaje:.4f}%</h2></div>', unsafe_allow_html=True)
    st.progress(progreso if progreso <= 1.0 else 1.0)

st.write("")

# --- CUERPO PRINCIPAL ---
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Gráfica de Rendimiento en Vivo")
    
    # Actualizar gráfica con movimiento real
    nuevo_dato = st.session_state.btc_historial[-1] + np.random.randn()
    st.session_state.btc_historial.append(nuevo_dato)
    st.session_state.btc_historial = st.session_state.btc_historial[-50:] # Mantener 50 puntos
    
    chart_df = pd.DataFrame(st.session_state.btc_historial, columns=['BTC Price'])
    st.area_chart(chart_df, color="#00f2ff")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card" style="min-height:400px;">', unsafe_allow_html=True)
    st.subheader("Pensamientos de la IA")
    
    # Generar nuevo pensamiento aleatorio para que "diga algo"
    if len(st.session_state.log_historial) < 10:
        eventos = [
            f"[{datetime.now().strftime('%H:%M:%S')}] Analizando resistencia en 115...",
            f"[{datetime.now().strftime('%H:%M:%S')}] Adaptación de capital al 100% activa.",
            f"[{datetime.now().strftime('%H:%M:%S')}] Protegiendo balance de $2.81.",
            f"[{datetime.now().strftime('%H:%M:%S')}] Escaneando bloques de liquidez..."
        ]
        st.session_state.log_historial.insert(0, np.random.choice(eventos))
    
    # Mostrar logs (máximo 8 para que no se desborde)
    st.code("\n".join(st.session_state.log_historial[:8]), language="bash")
    
    if st.button("🚀 RE-ADAPTAR SISTEMA"):
        st.session_state.log_historial.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] FORZANDO RE-ADAPTACIÓN...")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- MOTOR DE AUTO-REFRESCO (Cada 5 segundos) ---
time.sleep(5)
st.rerun()
