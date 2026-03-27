import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import hmac
import hashlib

# --- 1. CONFIGURACIÓN DE SEGURIDAD (TUS LLAVES) ---
# RECUERDA: En Bitso, la API debe tener permiso de "Colocar Órdenes"
API_KEY = "TU_API_KEY_AQUI"
API_SECRET = "TU_API_SECRET_AQUI"
NOMBRE_EMPRESA = "ANGEL PRESTIGE INVESTMENTS"

st.set_page_config(layout="wide", page_title=NOMBRE_EMPRESA, page_icon="⛩️")

# --- 2. MOTOR DE EJECUCIÓN (EL CEREBRO QUE COMPRA Y VENDE) ---
class MahoraExecutor:
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.url = "https://api.bitso.com"

    def _auth(self, method, path, body=""):
        nonce = str(int(time.time() * 1000))
        message = nonce + method + path + body
        signature = hmac.new(self.secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
        return {'Authorization': f'Bitso {self.key}:{nonce}:{signature}'}

    def ejecutar_operacion(self, book, side, amount):
        # Esta es la función que REALMENTE hace la compra o venta
        path = "/v3/orders/"
        # Para pruebas, usamos órdenes de mercado (se ejecutan al instante)
        payload = f'{{"book":"{book}","side":"{side}","type":"market","major":"{amount}"}}'
        
        # --- QUITA EL '#' DE ABAJO PARA QUE EL BOT EMPIECE A COMPRAR/VENDER REAL ---
        # response = requests.post(self.url + path, headers=self._auth("POST", path, payload), data=payload)
        # return response.json()
        return {"status": "Simulado", "msg": "Quita el '#' en el código para activar"}

# --- 3. LÓGICA DE GANANCIAS (TAKE PROFIT) ---
def analizar_y_actuar(precio_actual, rsi):
    # Si el RSI es mayor a 65, hay que vender para asegurar ganancias
    if rsi >= 65:
        return "VENDE (SELL)", "#ff00ff", "¡GANANCIA DETECTADA! Vendiendo para asegurar MXN."
    # Si el RSI es menor a 35, hay que comprar porque está barato
    elif rsi <= 35:
        return "COMPRA (BUY)", "#39FF14", "PRECIO BAJO. Comprando para acumular."
    else:
        return "ESPERA (HOLD)", "#00f2ff", "Manteniendo posición para maximizar retorno."

# --- 4. DISEÑO PRESTIGE (RESTABLECIDO) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.9)), url("{fondo_url}"); background-size: cover; color: white; }}
    .kpi-card {{ background: rgba(10, 25, 41, 0.85); border: 1px solid #00f2ff; border-radius: 12px; padding: 15px; text-align: center; }}
    .console-box {{ background: rgba(0, 0, 0, 0.9); border: 2px solid #ff00ff; border-radius: 10px; padding: 20px; font-family: monospace; color: #39FF14; height: 400px; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. INTERFAZ ---
st.markdown(f'<h1 style="text-align:center; color:#00f2ff;">⛩️ {NOMBRE_EMPRESA}</h1>', unsafe_allow_html=True)

# Simulamos datos para la vista (basado en tus capturas)
saldo_mxn = 114.29 # Tu saldo actual
rsi_mock = 68.0 # Simulamos que subió para que veas la señal de VENTA

label, color, msg = analizar_y_actuar(1226980, rsi_mock)

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="kpi-card"><small>MXN REAL</small><br><b style="font-size:22px;">${saldo_mxn}</b></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="kpi-card"><small>ACCIÓN IA</small><br><b style="color:{color}; font-size:22px;">{label}</b></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="kpi-card"><small>ESTADO</small><br><b style="color:#39FF14;">EJECUTANDO</b></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="kpi-card"><small>META</small><br><b style="color:#ff00ff;">1.14%</b></div>', unsafe_allow_html=True)

st.write("")
col_left, col_right = st.columns([2, 1])

with col_left:
    st.write("### 📈 MONITOREO DE ACTIVOS")
    # Gráfica simplificada para velocidad
    st.info(f"IA Pensamiento: {msg}")
    if label == "VENDE (SELL)":
        st.warning("⚠️ El bot está intentando vender para proteger tus ganancias.")

with col_right:
    st.markdown(f"""
        <div class="console-box">
            <b style="color:#ff00ff;">>> MAHORA SYSTEM LOG</b><br>
            [10:15:02] Analizando BTC/MXN...<br>
            [10:15:05] RSI ALTO: {rsi_mock}<br>
            [10:15:10] <span style="color:{color};">ACCIÓN: {label}</span><br>
            <br>
            <hr>
            <b>ESTRATEGIA CANADÁ:</b><br>
            Vendiendo para evitar que la caída te quite lo ganado.
        </div>
    """, unsafe_allow_html=True)

time.sleep(10)
st.rerun()
