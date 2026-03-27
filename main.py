import streamlit as st
import requests
import pandas as pd
import time
import hmac
import hashlib

# --- 1. CONFIGURACIÓN DE SEGURIDAD ---
API_KEY = "TU_API_KEY_AQUI"
API_SECRET = "TU_API_SECRET_AQUI"
NOMBRE_EMPRESA = "ANGEL PRESTIGE INVESTMENTS"
OBJETIVO_GANANCIA = 1.05  # Vende cuando ganes 5% (ajustable)

st.set_page_config(layout="wide", page_title=NOMBRE_EMPRESA, page_icon="⛩️")

# --- 2. LÓGICA DE VENTA AUTOMÁTICA ---
def ejecutar_venta_total(amount_btc):
    # Función para convertir todo tu BTC a MXN cuando hay ganancia
    path = "/v3/orders/"
    payload = f'{{"book":"btc_mxn","side":"sell","type":"market","major":"{amount_btc}"}}'
    nonce = str(int(time.time() * 1000))
    signature = hmac.new(API_SECRET.encode('utf-8'), (nonce + "POST" + path + payload).encode('utf-8'), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    
    # --- PARA ACTIVAR VENTA REAL, QUITA EL '#' DE ABAJO ---
    # response = requests.post("https://api.bitso.com" + path, headers=headers, data=payload)
    # return response.json()
    return {"status": "Simulado", "msg": "Venta lista para ejecutarse"}

# --- 3. DISEÑO PRESTIGE ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), url("{fondo_url}"); background-size: cover; color: white; }}
    .kpi-card {{ background: rgba(10, 25, 41, 0.9); border: 1px solid #ff00ff; border-radius: 12px; padding: 15px; text-align: center; }}
    .status-box {{ background: rgba(0,0,0,0.8); border: 2px solid #39FF14; padding: 20px; border-radius: 10px; font-family: monospace; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. INTERFAZ ---
st.markdown(f'<h1 style="text-align:center; color:#00f2ff;">⛩️ {NOMBRE_EMPRESA}</h1>', unsafe_allow_html=True)

# Datos actuales (Basados en tu reporte de $111)
saldo_actual = 111.00 #
precio_compra_promedio = 1220000.00 # Ejemplo de tu precio de entrada
precio_actual_btc = 1226000.00 # Precio de mercado

# Cálculo de ganancia
rendimiento = (precio_actual_btc / precio_compra_promedio)

c1, c2, c3 = st.columns(3)
c1.markdown(f'<div class="kpi-card"><small>SALDO ACTUAL</small><br><b style="font-size:24px;">${saldo_actual} MXN</b></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="kpi-card"><small>ESTADO DE VENTA</small><br><b style="color:#39FF14;">MONITOREANDO GANANCIA</b></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="kpi-card"><small>META CANADÁ</small><br><b style="color:#ff00ff;">1.11%</b></div>', unsafe_allow_html=True)

st.write("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🛡️ Protector de Capital")
    if saldo_actual < 115:
        st.error(f"⚠️ Alerta: Tu saldo de $111 está por debajo de los $120 de hace 3 días. El mercado está en caída.")
    
    if rendimiento >= OBJETIVO_GANANCIA:
        st.success("🚀 ¡OBJETIVO ALCANZADO! La IA recomienda vender ahora para asegurar ganancias.")
        if st.button("EJECUTAR VENTA MANUAL"):
            ejecutar_venta_total(0.00006301)
    else:
        st.info(f"Esperando que el precio suba un {(OBJETIVO_GANANCIA - rendimiento)*100:.2f}% más para vender con ganancia.")

with col2:
    st.markdown(f"""
        <div class="status-box">
            <b style="color:#39FF14;">>> LOG DE OPERACIONES</b><br>
            [LOG] Analizando histórico...<br>
            [LOG] Saldo inicial: $120<br>
            [LOG] Saldo actual: $111<br>
            [LOG] <span style="color:#ff00ff;">ACCIÓN: Protegiendo...</span><br>
            <br>
            <hr>
            <b>MAHORA PENSAMIENTO:</b><br>
            "No dejaremos que los $111 bajen más. En cuanto recuperemos nivel, cerramos posición."
        </div>
    """, unsafe_allow_html=True)

time.sleep(10)
st.rerun()
