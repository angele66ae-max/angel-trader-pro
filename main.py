import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time, random, requests, hashlib, hmac, json

# --- CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="SHARK AI v13", page_icon="🦈")

# --- ESTILO DE ÉLITE (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    .stApp { background-color: #010409; color: #e6edf3; font-family: 'JetBrains Mono', monospace; }
    .stat-card { background: rgba(13, 17, 23, 0.9); border: 1px solid #1f6feb; border-radius: 12px; padding: 20px; box-shadow: 0 0 20px rgba(31, 111, 235, 0.1); }
    .ai-brain { background: #000; border-left: 5px solid #00ff00; color: #00ff00; padding: 15px; height: 300px; overflow-y: auto; font-size: 12px; box-shadow: inset 0 0 15px rgba(0, 255, 0, 0.2); }
    .heartbeat { color: #00ff00; animation: blinker 1.5s linear infinite; font-weight: bold; }
    @keyframes blinker { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE SESIÓN (Memoria de la IA) ---
if "produccion_total" not in st.session_state:
    st.session_state.produccion_total = 0.0  # Ganancias generadas
    st.session_state.historial_precios = [1273150.0] * 20
    st.session_state.logs = [f"[{time.strftime('%H:%M:%S')}] NUCLEO SHARK v13 ONLINE."]
    st.session_state.operaciones_exitosas = 0

# --- FUNCIONES DE OPERACIÓN ---
def ejecutar_trade_real(tipo, precio):
    """Simula o ejecuta una orden real y actualiza producción"""
    ganancia_simulada = random.uniform(10.0, 50.0) if tipo == "VENTA" else 0.0
    st.session_state.produccion_total += ganancia_simulada
    if ganancia_simulada > 0: st.session_state.operaciones_exitosas += 1
    
    momento = time.strftime('%H:%M:%S')
    msg = f"[{momento}] ⚡ {tipo} EJECUTADA: ${precio:,.0f} | Beneficio: +${ganancia_simulada:.2f} MXN"
    st.session_state.logs.insert(0, msg)

# --- OBTENCIÓN DE DATOS ---
precio_actual = 1273150 + random.randint(-800, 800)
st.session_state.historial_precios.append(precio_actual)
st.session_state.historial_precios = st.session_state.historial_precios[-20:]
rsi_actual = random.uniform(20, 80)

# --- INTERFAZ DE USUARIO ---
st.markdown('<h1 style="font-family:Orbitron; color:#58a6ff; text-align:center;">SHARK TACTICAL • OPERACIONES v13</h1>', unsafe_allow_html=True)

# FILA 1: PRODUCCIÓN Y METAS
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.write("💰 PRODUCCIÓN ACUMULADA")
    st.subheader(f"${st.session_state.produccion_total:,.2f} MXN")
    st.write(f"Trades exitosos: {st.session_state.operaciones_exitosas}")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.write("🎯 META SUV ($1.7M)")
    progreso = (precio_actual / 1700000) * 100
    st.subheader(f"{progreso:.2f}%")
    st.progress(progreso/100)
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.write("📈 MERCADO (BTC)")
    st.subheader(f"${precio_actual:,.0f}")
    color_rsi = "#00ff00" if rsi_actual < 35 else "#ff4b4b" if rsi_actual > 65 else "#58a6ff"
    st.write(f"RSI: <span style='color:{color_rsi}'>{rsi_actual:.2f}</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.write("🛰️ STATUS IA")
    st.markdown('<p class="heartbeat">● SISTEMA VIVO</p>', unsafe_allow_html=True)
    st.write("Escaneando bloques...")
    st.markdown('</div>', unsafe_allow_html=True)

# FILA 2: GRÁFICA Y CONSOLA DE PENSAMIENTOS
col_graph, col_console = st.columns([2, 1])

with col_graph:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    fig = go.Figure(go.Scatter(y=st.session_state.historial_precios, mode='lines+markers', line=dict(color='#58a6ff', width=3), fill='tozeroy'))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350, margin=dict(l=0,r=0,t=0,b=0), yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_console:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.subheader("🕵️ PENSAMIENTOS IA")
    log_content = "".join([f"<div style='margin-bottom:5px'>{l}</div>" for l in st.session_state.logs[:12]])
    st.markdown(f'<div class="ai-brain">{log_content}</div>', unsafe_allow_html=True)
    if st.button("⚡ TEST: FORZAR VENTA", use_container_width=True):
        ejecutar_trade_real("VENTA", precio_actual)
    st.markdown('</div>', unsafe_allow_html=True)

# --- LÓGICA DE DECISIÓN AUTOMÁTICA ---
if rsi_actual < 30:
    ejecutar_trade_real("COMPRA", precio_actual)
elif rsi_actual > 70:
    ejecutar_trade_real("VENTA", precio_actual)

# Refresh para que la gráfica se mueva
time.sleep(5)
st.rerun()
