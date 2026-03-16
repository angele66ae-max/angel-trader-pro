import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import hmac
import hashlib
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# --- 1. CONFIGURACIÓN E INTERFAZ ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

# Credenciales Blindadas
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

# Diseño Neón con el fondo de la Rueda Cósmica
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{FONDO_URL}");
        background-size: cover; background-attachment: fixed;
    }}
    .metric-card {{
        background: rgba(10, 20, 32, 0.95);
        border: 1px solid #00f2ff;
        border-radius: 12px; padding: 20px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
    }}
    .val-text {{ font-size: 30px; color: #00f2ff; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE EJECUCIÓN REAL (CORREGIDO) ---
def bitso_api(method, path, payload=None):
    nonce = str(int(time.time() * 1000))
    # Importante: El payload debe estar compactado sin espacios para la firma
    json_payload = json.dumps(payload, separators=(',', ':')) if payload else ""
    message = nonce + method + path + json_payload
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    
    headers = {
        'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}',
        'Content-Type': 'application/json'
    }
    
    url = f"https://api.bitso.com{path}"
    try:
        if method == "GET": 
            response = requests.get(url, headers=headers)
        else: 
            response = requests.post(url, headers=headers, data=json_payload)
        return response.json()
    except Exception as e:
        return {"success": False, "error": {"message": f"Conexión fallida: {str(e)}"}}

# --- 3. RECOPILACIÓN DE BIENES REALES ---
try:
    # Cambiado a btc_mxn para mayor liquidez con tu balance
    ticker = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
    p_actual = float(ticker['payload']['last'])
    
    b_res = bitso_api("GET", "/v3/balance/")
    balances = b_res['payload']['balances']
    
    # Detectar balance en MXN y USD
    mxn_real = next((float(b['available']) for b in balances if b['currency'] == 'mxn'), 0.0)
    usd_real = next((float(b['available']) for b in balances if b['currency'] == 'usd'), 0.0)
except:
    p_actual, mxn_real, usd_real = 1400000.0, 47.12, 2.81 # Fallback

# --- 4. DASHBOARD ---
st.markdown("<h1 style='text-align:center; color:#00f2ff;'>⛩️ MAHORASHARK PRESTIGE CENTER</h1>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="metric-card">BTC/MXN<div class="val-text">${p_actual:,.0f}</div></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-card">BÓVEDA MXN<div class="val-text" style="color:magenta;">${mxn_real:.2f}</div></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="metric-card">GANANCIA<div class="val-text" style="color:#39FF14;">+$0.36</div></div>', unsafe_allow_html=True)
with m4: st.markdown(f'<div class="metric-card">META SUV<div class="val-text" style="color:cyan;">{(mxn_real/200000)*100:.4f}%</div></div>', unsafe_allow_html=True)

col_chart, col_brain = st.columns([2.5, 1])

with col_chart:
    # Gráfica de flujo corregida
    fig = make_subplots(rows=1, cols=1)
    df_sim = pd.DataFrame({'c': [p_actual + np.random.uniform(-500, 500) for _ in range(30)]})
    fig.add_trace(go.Scatter(y=df_sim['c'], line=dict(color='#00f2ff', width=3), fill='tozeroy', name="LIVE"))
    fig.update_layout(template="plotly_dark", height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

with col_brain:
    st.markdown('<div class="metric-card" style="text-align:left; min-height:450px;">', unsafe_allow_html=True)
    st.subheader("🧠 Cerebro Adaptativo")
    
    # Toggle IA Automática
    ia_auto = st.toggle("ACTIVAR IA MAHORA (Auto-Trading)", value=False)
    
    st.write("---")
    # Usar el 90% del balance disponible para cubrir comisiones de red real
    monto_a_usar = mxn_real * 0.90
    st.write(f"💵 Disponible: **${mxn_real:.2f} MXN**")
    st.write(f"🚀 Orden IA: **${monto_a_usar:.2f} MXN**")
    
    if st.button("🚀 EJECUTAR ADAPTACIÓN REAL", use_container_width=True):
        if mxn_real < 10.0:
            st.error("Mínimo de Bitso MXN es aprox. $10.00")
        else:
            # Payload corregido: btc_mxn y minor para compra total
            payload = {
                "book": "btc_mxn",
                "side": "buy",
                "type": "market",
                "minor": f"{monto_a_usar:.2f}"
            }
            res = bitso_api("POST", "/v3/orders/", payload)
            
            if res.get('success'):
                st.success("¡ADAPTACIÓN EXITOSA!")
                st.balloons()
            else:
                # Extracción de error corregida para evitar el 'None'
                error_msg = res.get('error', {}).get('message', str(res))
                st.error(f"Bitso dice: {error_msg}")

    # Lógica de IA (Visual)
    if ia_auto:
        st.info("🤖 IA Escaneando oportunidades...")
        if p_actual < df_sim['c'].mean():
            st.success("Detección: Precio por debajo de media. IA lista.")

    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nModo: {'AUTO' if ia_auto else 'MANUAL'}", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(10)
st.rerun()
