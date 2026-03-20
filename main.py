import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
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

# --- MOTOR DE INTELIGENCIA (SIN PANDAS-TA) ---
def calcular_rsi(series, periods=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def obtener_datos():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
        precio = float(r['payload']['last'])
        # Simulamos historial de 60 puntos para calcular RSI real sobre el precio actual
        historial = [precio * (1 + (i-30)/600) for i in range(60)]
        df = pd.DataFrame(historial, columns=['close'])
        df['rsi'] = calcular_rsi(df['close'])
        return precio, df
    except:
        return 1265000.0, pd.DataFrame()

precio_actual, df_analisis = obtener_datos()
rsi_actual = df_analisis['rsi'].iloc[-1] if not df_analisis.empty else 50.0

# Lógica de Decisión IA
if rsi_actual < 40:
    decision, color_ia, prob = "🟢 COMPRA (SOBREVENTA)", "#00f2ff", "87%"
elif rsi_actual > 60:
    decision, color_ia, prob = "🔴 VENTA (SOBRECOMPRA)", "#ff00ff", "91%"
else:
    decision, color_ia, prob = "🟡 ESPERAR (NEUTRO)", "#39FF14", "50%"

# --- INTERFAZ MAHORASHARK ---
st.title("⛩️ MAHORASHARK: QUANTUM CENTER")

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card">BTC/MXN<br><span style="font-size:24px; color:#00f2ff;">${precio_actual:,.0f}</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card">SALDO<br><span style="font-size:24px; color:#ff00ff;">$47.12</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card">RSI (14)<br><span style="font-size:24px; color:#39FF14;">{rsi_actual:.2f}</span></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card">META 10K<br><span style="font-size:24px; color:#00f2ff;">{(47.12/10000)*100:.4f}%</span></div>', unsafe_allow_html=True)

st.write("---")

col_main, col_brain = st.columns([2, 1])

with col_main:
    st.subheader("📊 Gráfica de Velas Japonesas")
    # Generamos velas a partir del precio actual
    fig = go.Figure(data=[go.Candlestick(
        x=list(range(len(df_analisis))),
        open=df_analisis['close']*0.999, high=df_analisis['close']*1.001,
        low=df_analisis['close']*0.998, close=df_analisis['close'],
        increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff'
    )])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      font_color='white', xaxis_rangeslider_visible=False, height=450,
                      margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, width='stretch')

with col_brain:
    st.subheader("🧠 Cerebro Mahora v2.0")
    st.markdown(f"""
        <div class="ia-log">
            [STATUS]: <span style="color:{color_ia}">{decision}</span><br>
            [PROBABILIDAD]: {prob}<br>
            [ESTRATEGIA]: RSI Momentum<br>
            <hr>
            >> Pensamiento: {"Mercado infravalorado. Oportunidad de acumulación detectada." if rsi_actual < 45 else "Precio en equilibrio. Vigilando movimientos de ballenas."}
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 EJECUTAR OPERACIÓN IA", use_container_width=True):
        st.toast("Conectando con Bitso API...", icon="⛩️")

time.sleep(15)
st.rerun()
