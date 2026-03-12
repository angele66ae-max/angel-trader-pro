import streamlit as st
import time
import requests
import hashlib
import hmac
import os
from dotenv import load_dotenv

# 1. Configuración de Seguridad
load_dotenv()
# En Streamlit Cloud, esto leerá automáticamente de tus "Secrets"
API_KEY = st.secrets.get("BITSO_API_KEY") or os.getenv("BITSO_API_KEY")
API_SECRET = st.secrets.get("BITSO_API_SECRET") or os.getenv("BITSO_API_SECRET")

class AngelTrader:
    def __init__(self):
        self.url_base = "https://api.bitso.com"

    def firmar_solicitud(self, metodo, endpoint, payload=""):
        nonce = str(int(time.time() * 1000))
        message = nonce + metodo + endpoint + payload
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
        return {"Authorization": f"Bitso {API_KEY}:{nonce}:{signature}", "Content-Type": "application/json"}

    def obtener_precio(self):
        try:
            r = requests.get(f"{self.url_base}/v3/ticker/?book=btc_mxn")
            return float(r.json()['payload']['last'])
        except: return None

    def comprar_btc(self, monto_mxn):
        endpoint = "/v3/orders/"
        payload = f'{{"book":"btc_mxn","side":"buy","type":"market","major":"{monto_mxn}"}}'
        headers = self.firmar_solicitud("POST", endpoint, payload)
        try:
            r = requests.post(f"{self.url_base}{endpoint}", data=payload, headers=headers)
            return r.json()
        except Exception as e: return {"status": "error", "message": str(e)}

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="ANGEL IA TRADER", page_icon="📈")
st.title("🚀 ANGEL IA - Trading Bot")

bot = AngelTrader()

# Mostrar precio actual
precio = bot.obtener_precio()
if precio:
    st.metric(label="Bitcoin (BTC/MXN)", value=f"${precio:,.2f}")
else:
    st.error("No se pudo obtener el precio. Revisa tu conexión.")

st.divider()

# Botón de compra
if st.button("PROBAR COMPRA ($10 MXN)", type="primary"):
    with st.spinner("Ejecutando orden en Bitso..."):
        res = bot.comprar_btc("10.00")
        if "payload" in res:
            st.success(f"✅ ¡Compra Exitosa! ID: {res['payload']['oid']}")
        else:
            error_msg = res.get('errors', [{'message': 'Error desconocido'}])[0]['message']
            st.error(f"❌ Error: {error_msg}")

# Lógica de Automatización (Simple)
st.sidebar.title("Configuración IA")
activar_ia = st.sidebar.toggle("Activar Scalping Automático")

if activar_ia:
    st.info("🤖 IA activada. El bot comprará automáticamente cuando detecte caídas.")
    # Aquí puedes agregar un loop simple o un refresh automático
