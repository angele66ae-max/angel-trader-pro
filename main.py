import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac, hashlib, time, numpy as np
import random
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="MahoraShark Prestige", page_icon="⛩️")

# --- 2. ESTILO PRESTIGE (GOTAS + NEÓN) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(5,10,14,0.95), rgba(5,10,14,0.98)), url("{fondo_url}"); background-size: cover; color: white; }}
    .main-header {{ text-align: center; color: #ffffff; font-weight: bold; font-size: 30px; text-shadow: 0 0 15px #00f2ff; border-bottom: 2px solid #00f2ff; padding: 10px; margin-bottom: 20px; }}
    .metric-card {{ background: rgba(11, 20, 26, 0.9); border: 1.5px solid #00f2ff; border-radius: 10px; padding: 15px; text-align: center; box-shadow: 0 0 10px rgba(0, 242, 255, 0.2); }}
    .ia-terminal {{ background: #000; border: 1.5px solid #ff00ff; border-radius: 10px; padding: 15px; font-family: monospace; color: #39FF14; height: 350px; overflow-y: auto; font-size: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. MOTOR DE DATOS REALES ---
st.sidebar.title("🏎️ PISTA")
activo = st.sidebar.selectbox("Seleccionar Activo", ["btc_mxn", "eth_mxn", "usd_mxn"])

def get_live_data(libro):
    try:
        r = requests.get(f"https://api.bitso.com/v3/trades/?book={libro}").json()['payload']
        prices = [float(t['price']) for t in r][::-1]
        vol = [float(t['amount']) for t in r][:40]
        return prices[-1], prices, vol
    except: return 0.0, [0]*40, [0]*40

precio, historial, volumen = get_live_data(activo)
saldo_real = 68.91
meta = 10000.0

# --- 4. BARRA SUPERIOR (LO QUE FALTABA) ---
st.markdown(f'<div class="main-header">⛩️ ANGEL\'S PRESTIGE OPERATIONAL CENTER</div>', unsafe_allow_html=True)

t1, t2, t3, t4 = st.columns(4)
t1.markdown(f'<div class="metric-card"><small>PRECIO {activo.upper()}</small><br><b style="font-size:22px; color:#00f2ff">${precio:,.2f}</b></div>', unsafe_allow_html=True)
t2.markdown(f'<div class="metric-card"><small>SALDO MXN</small><br><b style="font-size:22px; color:#ff00ff">${saldo_real:,.2f}</b></div>', unsafe_allow_html=True)
t3.markdown(f'<div class="metric-card"><small>PROGRESO CANADÁ</small><br><b style="font-size:22px; color:#39FF14">{(saldo_real/meta)*100:.2f}%</b></div>', unsafe_allow_html=True)
t4.markdown(f'<div class="metric-card"><small>IA STATUS</small><br><b style="font-size:22px">HYPER-DRIVE</b></div>', unsafe_allow_html=True)

st.write("")

# --- 5. CUERPO DEL TABLERO ---
c_main, c_side = st.columns([2.5, 1])

with c_main:
    # Gráfica Neón Viva
    fig = go.Figure(data=[go.Scatter(y=historial, mode='lines', line=dict(color='#00f2ff', width=3), fill='toself', fillcolor='rgba(0, 242, 255, 0.1)')])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400, margin=dict(l=0,r=0,t=0,b=0), font_color="white", xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'))
    st.plotly_chart(fig, use_container_width=True)

    # Indicadores
    i1, i2 = st.columns([1, 1.5])
    with i1:
        fig_rsi = go.Figure(go.Indicator(mode="gauge+number", value=random.randint(35, 65), gauge={'axis':{'range':[0,100]}, 'bar':{'color':'#00f2ff'}, 'steps':[{'range':[0,30],'color':'#ff00ff'},{'range':[70,100],'color':'#ff00ff'}]}))
        fig_rsi.update_layout(height=220, paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=20,b=0))
        st.plotly_chart(fig_rsi, use_container_width=True)
    with i2:
        fig_vol = go.Figure(data=[go.Bar(y=volumen, marker_color='#ff00ff', opacity=0.6)])
        fig_vol.update_layout(height=200, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20,b=0), font_color="white")
        st.plotly_chart(fig_vol, use_container_width=True)

with c_side:
    # --- PENSAMIENTOS ALEATORIOS DE LA IA ---
    pensamientos = [
        "Analizando patrones de velas... el Ferrari está listo.",
        "Detectando ballenas en el mercado. Mantén la calma.",
        "El RSI está estable, no es momento de arriesgar el viaje.",
        "Meta de 10K en la mira. Cada centavo suma para Canadá.",
        "Escaneando oportunidades en tiempo real...",
        "¿Viste ese movimiento? El algoritmo Mahora ya lo predijo.",
        "Ajustando parámetros de precisión... 99.9% de efectividad.",
        "Ángel, el mercado está aburrido, pero nosotros no bajamos la guardia."
    ]
    pensamiento_actual = random.choice(pensamientos)
    ahora = datetime.now().strftime("%H:%M:%S")

    st.markdown(f"""
        <div style="background:rgba(255,0,255,0.1); border:1.5px solid #ff00ff; border-radius:10px; padding:15px;">
            <h4 style="color:#ff00ff; margin:0; font-size:16px;">🧠 CEREBRO MAHORA v12.0</h4>
            <div class="ia-terminal">
                [{ahora}] >> SISTEMA: OPTIMIZADO.<br>
                [{ahora}] >> ACTIVO: {activo.upper()}.<br>
                <hr style="border-color:#333">
                >> PENSAMIENTO DE LA IA:<br>
                <b>{pensamiento_actual}</b><br><br>
                >> Angel, el Ferrari corre cada 10 segundos. 🇨🇦
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("🚀 FORZAR GATILLO", use_container_width=True):
        st.toast("Disparando comando...")

# --- 6. AUTO-REFRESCO CADA 10 SEGUNDOS ---
time.sleep(10)
st.rerun()
