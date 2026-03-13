import streamlit as st
import time, requests, random
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="SHARK AI MONITOR", page_icon="🦈")

# --- ESTILO MEJORADO ---
st.markdown("""
<style>
    .log-container {
        background-color: rgba(0, 255, 0, 0.05);
        border-left: 3px solid #00ff00;
        padding: 10px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        height: 250px;
        overflow-y: auto;
    }
    .status-active { color: #00ff00; font-weight: bold; }
    .status-wait { color: #ffaa00; }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE MEMORIA DE LA IA ---
if "logs" not in st.session_state:
    st.session_state.logs = [f"[{time.strftime('%H:%M:%S')}] SHARK AI Iniciado. Esperando órdenes..."]

# --- FUNCIÓN DE ANÁLISIS REAL ---
def shark_analysis(precio, rsi):
    momento = time.strftime('%H:%M:%S')
    if rsi < 30:
        msg = f"[{momento}] 🟢 SEÑAL DE COMPRA: RSI en {rsi:.2f}. El mercado está barato."
    elif rsi > 70:
        msg = f"[{momento}] 🔴 SEÑAL DE VENTA: RSI en {rsi:.2f}. Posible caída próxima."
    else:
        msg = f"[{momento}] ⚪ ANALIZANDO: BTC a ${precio:,.0f}. Esperando cambio en RSI ({rsi:.2f})."
    
    # Guardar solo los últimos 10 eventos
    st.session_state.logs.insert(0, msg)
    st.session_state.logs = st.session_state.logs[:10]

# --- DATOS (Simulación mejorada para testeo) ---
precio_actual = 1278010 # Valor de tu última captura
rsi_actual = random.uniform(25, 75) # Esto vendrá de tu API Bitso

# --- INTERFAZ ---
st.title("🦈 SHARK AI: CENTRO DE CONTROL")

col_main, col_side = st.columns([2, 1])

with col_main:
    # Gráfico de Mercado
    fig = go.Figure(go.Scatter(y=[precio_actual-100, precio_actual+50, precio_actual], fill='tozeroy', line_color='#00eaff'))
    fig.update_layout(height=400, margin=dict(l=0,r=0,t=0,b=0), template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col_side:
    st.subheader("🕵️ PENSAMIENTOS DE LA IA")
    # Este es el cuadro que te dice qué está haciendo
    log_html = "".join([f"<div>{line}</div>" for line in st.session_state.logs])
    st.markdown(f'<div class="log-container">{log_html}</div>', unsafe_allow_html=True)
    
    st.write("")
    if st.button("🚀 FORZAR ANÁLISIS AHORA", use_container_width=True):
        shark_analysis(precio_actual, rsi_actual)
        st.rerun()

# Dashboard Inferior
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("PRECIO BTC", f"${precio_actual:,.0f} MXN")
with c2:
    st.metric("FUERZA RSI", f"{rsi_actual:.2f}")
with c3:
    # Progreso hacia la SUV de 1.7M
    progreso = (precio_actual / 1700000) * 100
    st.metric("META SUV $1.7M", f"{progreso:.1f}%")

# Ejecutar análisis automático si la IA está activa
if st.session_state.get("ai_on", True):
    shark_analysis(precio_actual, rsi_actual)
    time.sleep(10)
    st.rerun()
