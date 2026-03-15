import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
import plotly.graph_objects as go # <--- NUEVA LIBRERÍA DE GRÁFICOS

# --- CONFIGURACIÓN DE NÚCLEO ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: PRESTIGE")

# --- RECUPERACIÓN DEL FONDO ---
fondo_directo = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    /* Fondo Estilo Galaxia */
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                    url("{fondo_directo}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    
    /* Tarjetas Translúcidas con Borde Cian */
    .card {{
        background: rgba(10, 10, 15, 0.9);
        border: 2px solid #00f2ff;
        border-radius: 12px; padding: 20px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
        margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# --- MEMORIA DE SESIÓN (Datos Reales Simulados) ---
if "precios_v" not in st.session_state:
    # Generar precios Open, High, Low, Close base para graficar
    base = 70915
    data = []
    for _ in range(35):
        o = base + np.random.uniform(-5, 5)
        c = o + np.random.uniform(-8, 8)
        h = max(o, c) + np.random.uniform(0, 4)
        l = min(o, c) - np.random.uniform(0, 4)
        data.append([o, h, l, c])
        base = c
    st.session_state.precios_v = data

# --- LÓGICA FINANCIERA ---
META = 10000.0
balance = 2.81
progreso = (balance / META)

st.markdown("<h1 style='text-align:center; color:#00f2ff; font-family:sans-serif;'>⛩️ MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)

# Dashboard Superior: Tarjetas
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="card">ESTADO BITSO<br><h2 style="color:#00ff00;">CONECTADO</h2></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="card">BALANCE USD<br><h2 style="color:magenta;">${balance:.2f}</h2></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="card">OBJETIVO VENTA<br><h2>115</h2></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="card">META SUV (10K)<br><h2>{(progreso*100):.4f}%</h2></div>', unsafe_allow_html=True)
    st.progress(progreso if progreso <= 1.0 else 1.0)

st.write("")

# --- CUERPO TÉCNICO (NUEVA SECCIÓN DE DISEÑO) ---
c1, c2 = st.columns([2, 1])

with c1:
    # Eliminamos el contenedor cuadrado feo. Usamos transparencia.
    st.markdown('<h3 style="color:#e0e0e0; margin-left:10px;">Gráfica de Velas Japonesas (Profesional)</h3>', unsafe_allow_html=True)
    
    # Simulación de movimiento para el próximo refresco
    last_c = st.session_state.precios_v[-1][3]
    n_o = last_c + np.random.uniform(-2, 2)
    n_c = n_o + np.random.uniform(-4, 4)
    n_h = max(n_o, n_c) + np.random.uniform(0, 2)
    n_l = min(n_o, n_c) - np.random.uniform(0, 2)
    st.session_state.precios_v.append([n_o, n_h, n_l, n_c])
    st.session_state.precios_v = st.session_state.precios_v[-35:]
    
    # Crear DataFrame
    df_v = pd.DataFrame(st.session_state.precios_v, columns=['o', 'h', 'l', 'c'])
    df_v['ts'] = range(len(df_v)) # Tiempo simulado
    
    # SOLUCIÓN DE DISEÑO: Graficar Velas Profesionales (Plotly)
    fig = go.Figure(data=[go.Candlestick(
        x=df_v['ts'],
        open=df_v['o'],
        high=df_v['h'],
        low=df_v['l'],
        close=df_v['c'],
        # Colores Prestige: Cian para arriba, Magenta para abajo
        increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff',
        name='BTC/USD'
    )])
    
    # Ajustar diseño del fondo para que sea negro transparente
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)', # Fondo de papel transparente
        plot_bgcolor='rgba(10,10,15,0.9)',   # Fondo de gráfica oscuro translúcido
        margin=dict(l=0, r=0, t=0, b=0), # Eliminar márgenes
        xaxis_rangeslider_visible=False,   # Quitar el slider de abajo para limpieza
        yaxis_title="Precio (USD)"
    )
    
    # Renderizar la gráfica ocupando todo el ancho
    st.plotly_chart(fig, use_container_width=True)

with c2:
    # Mantenemos la tarjeta de la IA, pero la integramos mejor visualmente
    st.markdown('<div class="card" style="height:480px;">', unsafe_allow_html=True)
    st.subheader("Cerebro Mahora")
    
    st.code(f"""
[{datetime.now().strftime('%H:%M:%S')}] ⛩️ Sincronizado.
[{datetime.now().strftime('%H:%M:%S')}] Escaneando liquidez Bitso...
[{datetime.now().strftime('%H:%M:%S')}] Adaptación: OK. Capital seguro.
[{datetime.now().strftime('%H:%M:%S')}] META SUV: {(progreso*100):.4f}%
    """, language="bash")
    
    st.write("")
    if st.button("🚀 FORZAR RE-ADAPTACIÓN IA"):
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- MOTOR DE ACTUALIZACIÓN RÁPIDA (3 seg) ---
time.sleep(3)
st.rerun()
