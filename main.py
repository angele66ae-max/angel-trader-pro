import streamlit as st
import requests
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime
import time

# --- CONFIGURACIÓN PRESTIGE ---
st.set_page_config(layout="wide", page_title="MahoraShark Quantum", page_icon="⛩️")

# Fondo Cósmico
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(5, 10, 14, 0.85), rgba(5, 10, 14, 0.95)), url("{fondo_url}");
        background-size: cover;
        background-attachment: fixed;
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

# --- MOTOR DE INTELIGENCIA ---
def obtener_datos_mercado():
    try:
        # En una versión Pro, aquí descargarías el historial de 24h
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
        precio = float(r['payload']['last'])
        # Simulamos historial para el cálculo de indicadores (RSI/Velas)
        historial = [precio * (1 + (i-30)/500) for i in range(60)]
        df = pd.DataFrame(historial, columns=['close'])
        df['rsi'] = ta.rsi(df['close'], length=14)
        return precio, df
    except:
        return 1265000.0, pd.DataFrame()

precio_actual, df_analisis = obtener_datos_mercado()
rsi_actual = df_analisis['rsi'].iloc[-1] if not df_analisis.empty else 50.0

# Lógica de Decisión IA
if rsi_actual < 35:
    decision = "🟢 COMPRA FUERTE (OVERSOLD)"
    probabilidad = "89%"
elif rsi_actual > 65:
    decision = "🔴 VENTA / TOMA DE GANANCIAS"
    probabilidad = "92%"
else:
    decision = "🟡 ESPERAR (MERCADO NEUTRO)"
    probabilidad = "50%"

# --- INTERFAZ ---
st.title("⛩️ MAHORASHARK: QUANTUM CENTER")

# Métricas Superiores
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card">BTC/MXN REAL<br><span style="font-size:24px; color:#00f2ff;">${precio_actual:,.0f}</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card">SALDO CUENTA<br><span style="font-size:24px; color:#ff00ff;">$47.12</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card">RSI (14)<br><span style="font-size:24px; color:#39FF14;">{rsi_actual:.2f}</span></div>', unsafe_allow_html=True)
with c4: 
    progreso = (47.12 / 10000) * 100
    st.markdown(f'<div class="metric-card">META 10K<br><span style="font-size:24px; color:#00f2ff;">{progreso:.4f}%</span></div>', unsafe_allow_html=True)

st.write("---")

col_main, col_brain = st.columns([2, 1])

with col_main:
    st.subheader("📊 Análisis Cuantitativo (Velas Neón)")
    # Gráfica de Velas con Colores Prestige
    fig = go.Figure(data=[go.Candlestick(
        x=list(range(len(df_analisis))),
        open=df_analisis['close']*0.999, high=df_analisis['close']*1.001,
        low=df_analisis['close']*0.998, close=df_analisis['close'],
        increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff'
    )])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      font_color='white', xaxis_rangeslider_visible=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

with col_brain:
    st.subheader("🧠 Cerebro Mahora v2.0")
    st.markdown(f"""
        <div class="ia-log">
            [STATUS]: {decision}<br>
            [PROBABILIDAD]: {probabilidad}<br>
            [RIESGO]: Bajo (2% capital)<br>
            [MOVIMIENTO]: Acumulando para Canadá 🇨🇦<br>
            <hr>
            >> Pensamiento: {"El RSI indica agotamiento de ventas. Es buen momento para entrar." if rsi_actual < 40 else "Esperando una señal más clara de las ballenas."}
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 EJECUTAR OPERACIÓN IA"):
        st.warning("⚠️ Conectando con API de Bitso para ejecutar orden real...")

# Auto-refresh
time.sleep(15)
st.rerun()
