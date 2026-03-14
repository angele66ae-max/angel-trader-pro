import streamlit as st
import pandas as pd
import numpy as np
import time
import hmac
import hashlib
import requests

# Intentamos importar pilot, si falla mostramos un mensaje amigable en lugar de romper la app
try:
    from pilot import pilot_process
except ImportError:
    pilot_process = None

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SHARK AI: PRESTIGE CENTER", layout="wide")

# --- ESTILO PERSONALIZADO (MAHORA ADAPTATION) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    .log-container { 
        background-color: #000; 
        color: #00ff00; 
        padding: 15px; 
        border-radius: 5px; 
        border: 1px solid #00ff00; 
        font-family: 'Courier New', monospace;
        height: 200px;
        overflow-y: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CREDENCIALES (REEMPLAZAR CON TUS LLAVES REALES) ---
API_KEY = "TU_API_KEY"
API_SECRET = "TU_API_SECRET"

def bitso_auth_request(method, path, payload=None):
    nonce = str(int(time.time() * 1000))
    message = nonce + method + path
    if payload:
        message += payload
    
    signature = hmac.new(API_SECRET.encode('utf-8'),
                         message.encode('utf-8'),
                         hashlib.sha256).hexdigest()
    
    auth_header = f"Bitso {API_KEY}:{nonce}:{signature}"
    url = f"https://api.bitso.com{path}"
    headers = {"Authorization": auth_header, "Content-Type": "application/json"}
    
    try:
        if method == "POST":
            response = requests.post(url, headers=headers, data=payload)
        else:
            response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# --- HEADER ---
st.title("🦈 SHARK AI: TERMINAL DE PRESTIGIO")
st.caption("MAHORA ADAPTATION PROTOCOL v19.3")

# --- MÉTRICAS PRINCIPALES ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("MERCADO DE BTC", "70,961 $", "USD")

with col2:
    # Basado en tu captura: $2.81 USD
    st.metric("SALDO DISPONIBLE", "2.81 $", "-0.08%")

with col3:
    st.metric("MOTOR DE IA", "ACTIVOS", "v10.1 CORE")

with col4:
    st.metric("OBJETIVO SUV", "90.2%", "PROGRESS")
    st.progress(0.902)

# --- CUERPO PRINCIPAL ---
c_left, c_right = st.columns([2, 1])

with c_left:
    st.subheader("Live Analysis")
    # Generamos datos aleatorios para el gráfico de tu captura
    chart_data = pd.DataFrame(
        np.random.randn(20, 1) + 70961,
        columns=['BTC Price']
    )
    st.area_chart(chart_data, color="#008080")

with c_right:
    st.markdown('<p style="font-size:18px;">🕵️ PENSAMIENTOS DE LA IA</p>', unsafe_allow_html=True)
    
    if st.button("🚀 DEPLOY AI (MODO REAL)"):
        st.info("Iniciando protocolo de adaptación...")
    
    # Contenedor de Logs (Corregido el error de sintaxis de la línea 97)
    log_time = time.strftime("[%H:%M:%S]")
    st.markdown(f"""
        <div class="log-container">
            {log_time} SISTEMA INICIADO. OPERADOR: PAVO FREE FIRE<br>
            [ADAPTACIÓN]: Analizando volatilidad...<br>
            [BITSO]: Conexión establecida con éxito.<br>
            [OBJETIVO]: Venta programada en 115.
        </div>
    """, unsafe_allow_html=True)

# --- LÓGICA DE TRADING (Corregido el error de la línea 69) ---
st.divider()
if st.checkbox("Mostrar panel de control técnico"):
    if st.button("Ejecutar Orden Manual"):
        # Payload formateado correctamente como JSON string
        payload_data = '{"book": "btc_mxn", "side": "buy", "type": "market", "major": "0.01"}'
        res = bitso_auth_request("POST", "/v3/orders", payload_data)
        st.write(res)

# Verificación del módulo Pilot
if pilot_process is None:
    st.warning("⚠️ El archivo 'pilot.py' no se encuentra en el directorio. La IA funcionará en modo simulado.")
    
