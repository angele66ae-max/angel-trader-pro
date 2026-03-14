import streamlit as st
import time, hashlib, hmac, json, requests

# --- CONFIGURACIÓN TÁCTICA ---
st.set_page_config(layout="wide", page_title="SHARK AI BLACK OPS")
st.markdown("<h1 style='text-align:center; color:cyan;'>🦈 SHARK AI: TERMINAL DE PRESTIGIO</h1>", unsafe_allow_html=True)

# --- CARGA DE LLAVES ---
try:
    API_KEY = st.secrets["BITSO_API_KEY"]
    API_SECRET = st.secrets["BITSO_API_SECRET"]
except Exception as e:
    st.error("🚨 ERROR EN SECRETS: Revisa tu archivo .streamlit/secrets.toml")
    st.stop()

# --- MOTOR DE BITSO ---
def bitso_api(method, path, payload=None):
    nonce = str(int(time.time() * 1000))
    json_payload = json.dumps(payload) if payload else ""
    message = nonce + method + path + json_payload
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}', 'Content-Type': 'application/json'}
    url = f"https://api.bitso.com{path}"
    
    if method == "POST":
        return requests.post(url, headers=headers, data=json_payload).json()
    return requests.get(url, headers=headers).json()

# --- OBTENER DATOS REALES ---
def cargar_datos():
    # Balance Real
    b = bitso_api("GET", "/v3/balance")
    usd = next((i['available'] for i in b['payload']['balances'] if i['currency'] == 'usd'), "0")
    # Precio Real
    t = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
    precio = t['payload']['last']
    return float(usd), float(precio)

# --- INTERFAZ ---
usd_real, precio_actual = cargar_datos()

col1, col2, col3 = st.columns(3)
col1.metric("SALDO DISPONIBLE", f"${usd_real} USD")
col2.metric("PRECIO BTC", f"${precio_actual} USD")
col3.metric("META SUV", "90.2%") # Tu meta actualizada

st.divider()

if st.button("🚀 DEPLOY AI (MODO REAL)"):
    st.session_state.live = True
    st.success("TIBURÓN EN EL AGUA: BUSCANDO SEÑALES...")

if st.session_state.get("live", False):
    # Aquí el bot operará con tu saldo de $2.81 USD
    st.info("Escaneando mercado...")
    # Ejemplo de compra real
    # bitso_api("POST", "/v3/orders", {"book": "btc_usd", "side": "buy", "type": "market", "major": "1.00"})
    time.sleep(5)
    st.rerun()
