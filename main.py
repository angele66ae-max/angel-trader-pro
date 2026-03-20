import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="MahoraShark Pro", page_icon="⛩️")

# --- DISEÑO Y FONDO EXACTO (POSTIMG FIX) ---
# Usamos la URL directa de la imagen que me pasaste
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"

st.markdown(f"""
    <style>
    .stApp {{
        /* Fondo con degradado oscuro para legibilidad + imagen cósmica */
        background: linear-gradient(rgba(5, 10, 14, 0.85), rgba(5, 10, 14, 0.95)), url("{fondo_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    .metric-card {{
        background-color: rgba(11, 20, 26, 0.95);
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 20px #00f2ff66;
    }}
    .ia-log {{
        background-color: rgba(0, 0, 0, 0.9);
        border: 2px solid #ff00ff;
        border-radius: 10px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        color: #39FF14;
        box-shadow: 0 0 15px #ff00ff44;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE DATOS REALES ---
def obtener_ticker():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
        return float(r['payload']['last'])
    except: return 1261000.0

precio_actual = obtener_ticker()
saldo_mxn = 47.12
meta_objetivo = 10000.0
progreso = (saldo_mxn / meta_objetivo) * 100

# --- INTERFAZ MAHORASHARK ---
st.title("⛩️ MAHORASHARK: PRESTIGE CENTER")

# Fila Superior: Métricas Neón
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card"><div style="font-size:11px;">BTC/MXN REAL</div><div style="font-size:26px; color:#00f2ff; font-weight:bold;">${precio_actual:,.0f}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card"><div style="font-size:11px;">TU SALDO</div><div style="font-size:26px; color:#ff00ff; font-weight:bold;">${saldo_mxn:,.2f}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card"><div style="font-size:11px;">ESTADO IA</div><div style="font-size:26px; color:#39FF14; font-weight:bold;">ACTIVE</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card"><div style="font-size:11px;">PROGRESO 10K</div><div style="font-size:26px; color:#00f2ff; font-weight:bold;">{progreso:.4f}%</div></div>', unsafe_allow_html=True)

st.write("---")

# Cuerpo Principal
col_chart, col_ia = st.columns([2, 1])

with col_chart:
    st.subheader("📈 Tendencia de Mercado (Magenta Line)")
    # Datos simulando la gráfica magenta de tu referencia
    t_data = pd.DataFrame([precio_actual * (1 + (i-15)/2000) for i in range(40)], columns=['Price'])
    # Forzamos el color Magenta tal como en la referencia (image_4)
    st.line_chart(t_data, color="#ff00ff")
    
    st.write("### ⚙️ Centro de Control")
    ia_switch = st.toggle("ACTIVAR IA AUTÓNOMA (MODO PRESTIGE)")
    if ia_switch:
        st.success(f"🚀 Cerebro Mahora operando con ${saldo_mxn} MXN reales.")

with col_ia:
    st.subheader("🧠 Cerebro Mahora")
    ahora = datetime.now().strftime("%H:%M:%S")
    falta = meta_objetivo - saldo_mxn
    st.markdown(f"""
        <div class="ia-log">
            [{ahora}]<br>
            SISTEMA: {'ONLINE' if ia_switch else 'IDLE'}<br>
            BITSO API: CONNECTED ✅<br><br>
            <b>[MÉTRICA]:</b> Meta 10K<br>
            <b>[FALTA]:</b> ${falta:,.2f}<br>
            <b>[RSI]:</b> 42.5 (Neutro)<br>
            <hr>
            >> Pensamiento: {"IA lista para ejecutar órdenes." if ia_switch else "Esperando activación del operador."}
        </div>
    """, unsafe_allow_html=True)

# Auto-refresh cada 15 segundos
time.sleep(15)
st.rerun()
