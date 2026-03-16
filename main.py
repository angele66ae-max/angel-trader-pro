import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import time

# Intentamos cargar acciones sin que se rompa el sistema
try:
    import yfinance as yf
    ACCIONES_LISTAS = True
except ImportError:
    ACCIONES_LISTAS = False

# --- 1. CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="MAHORASHARK AUTO-PILOT")

# Tus activos reales
MI_BTC = 0.00003542
META_USD = 115.00

st.markdown("<h1 style='color:#00f2ff; text-align:center;'>⛩️ MAHORASHARK: AUTO-PILOT ACTIVO</h1>", unsafe_allow_html=True)

# Contenedores dinámicos para que la página no parpadee
status_ia = st.empty()
monitor_stats = st.empty()
log_terminal = st.empty()

# --- 2. CEREBRO DE ADAPTACIÓN AUTOMÁTICA ---
def ejecutar_ia_autonoma():
    while True:
        try:
            # Sincronización de precio real
            r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
            p_actual = float(r['payload']['last'])
            valor_btc = MI_BTC * p_actual
            progreso = (valor_btc / META_USD) * 100
            
            # Verificación de saldo disponible
            # Nota: Cambia estos valores a tus llaves API para que sean dinámicos
            saldo_mxn = 0.00 
            saldo_usd = 0.22 

            # Mostrar métricas en tiempo real
            with monitor_stats.container():
                m1, m2, m3 = st.columns(3)
                m1.metric("Bóveda BTC (USD)", f"${valor_btc:.2f}")
                m2.metric("Saldo Disponible", f"${saldo_mxn} MXN")
                m3.metric("Meta ($115)", f"{progreso:.4f}%")

            # --- LÓGICA DE DECISIÓN AUTÓNOMA ---
            # La IA decide sola: Si hay saldo > $1 USD o $10 MXN, intenta comprar
            if saldo_mxn >= 10.0 or saldo_usd >= 1.0:
                status_ia.success("🚀 IA: ¡OPORTUNIDAD DETECTADA! Ejecutando compra automática...")
                # Aquí iría la orden real a la API
                time.sleep(2)
            else:
                # El bot se mantiene escaneando si no hay fondos suficientes
                status_ia.warning(f"🤖 IA: Escaneando... Esperando saldo mínimo ($10 MXN / $1 USD)")

            # Radar de Acciones (Si yfinance está instalado)
            if ACCIONES_LISTAS:
                # La IA monitorea Tesla automáticamente como activo secundario
                tsla = yf.Ticker("TSLA")
                p_tsla = tsla.history(period="1d")['Close'].iloc[-1]
                st.write(f"📈 Monitor Stock: TSLA a ${p_tsla:.2f} USD")

            with log_terminal:
                st.code(f"[{datetime.now().strftime('%H:%M:%S')}] IA Escaneando... Status: PRESTIGE | Modo: AUTO", language="bash")

        except Exception as e:
            # Corregido: El paréntesis y las comillas ahora cierran correctamente
            st.error(f"Error en el sistema: {str(e)}")
            
        time.sleep(20) # Ciclo de escaneo automático
        st.rerun()

# --- 3. INTERRUPTOR DE ENCENDIDO ---
activar = st.toggle("⚡ INICIAR CEREBRO AUTÓNOMO", value=True)

if activar:
    ejecutar_ia_autonoma()
else:
    st.info("Sistema en pausa. Active el interruptor para iniciar la compra automática.")
