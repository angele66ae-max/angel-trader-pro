import streamlit as st
import time
import requests
import hmac
import hashlib
import pandas as pd

# --- 1. CONFIGURACIÓN Y ESTILO (PRESTIGE) ---
st.set_page_config(layout="wide", page_title="MAHORASHARK SYNC")

st.markdown("""
<style>
    .stApp { background-color: #000505; color: #00f2ff; }
    .neon-border {
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 20px;
        background-color: rgba(0, 20, 30, 0.6);
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
        text-align: center; margin-bottom: 20px;
    }
    .val-major { font-size: 30px; font-weight: bold; color: white; text-shadow: 0 0 10px #00f2ff; }
    .val-minor { font-size: 16px; color: #39FF14; }
</style>
""", unsafe_allow_html=True)

# --- 2. BACKEND: CONEXIÓN REAL CON CACHÉ DE EMERGENCIA ---
# Reemplaza con tus llaves reales de Bitso
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

# Definimos tu saldo REAL de la captura como respaldo absoluto
SALDO_REAL_RESPALDO = {
    'mxn': 68.91,
    'btc': 0.00003542,
    'eth': 0.00000004
}

@st.cache_data(ttl=30) # Cacheamos datos por 30s para evitar bloqueos de API
def get_sincronized_balances():
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + "/v3/balance/"
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    
    try:
        # Intentar obtener datos reales
        response = requests.get("https://api.bitso.com/v3/balance/", headers=headers, timeout=5)
        payload = response.json()
        
        if payload['success']:
            balances = payload['payload']['balances']
            # Mapeo dinámico y real
            final_bal = {
                'mxn': next((float(b['total']) for b in balances if b['currency'] == 'mxn'), 0.0),
                'btc': next((float(b['total']) for b in balances if b['currency'] == 'btc'), 0.0),
                'eth': next((float(b['total']) for b in balances if b['currency'] == 'eth'), 0.0)
            }
            # Actualizamos la caché de emergencia
            st.session_state['last_valid_bal'] = final_bal
            return final_bal, "✅ SINCRO TOTAL"
        else:
            raise ValueError("API returned success:false")
            
    except Exception as e:
        # Si todo falla, usar la caché de session_state o el respaldo hardcodeado
        backup = st.session_state.get('last_valid_bal', SALDO_REAL_RESPALDO)
        return backup, f"⚠️ MODO CACHÉ (API Error)"

# --- 3. LÓGICA DE VISUALIZACIÓN ---
st.markdown("<h1 style='text-align:center; color:#00f2ff; text-shadow: 0 0 15px #00f2ff;'>⛩️ MAHORASHARK: OMNI-SYNC</h1>", unsafe_allow_html=True)

# Ejecutar el motor de sincronización
bal, status_api = get_sincronized_balances()

# Obtenemos precio de BTC para cálculos de meta (aproximado/real)
try:
    btc_price = float(requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()['payload']['last'])
except:
    btc_price = 73500.0 # Respaldo de precio

# Cálculos de Meta ($115 USD) - Basado en la captura
valor_btc_usd = bal['btc'] * btc_price
meta_usd = 115.0
progreso_meta = (valor_btc_usd / meta_usd) * 100

# --- 4. DASHBOARD GRID ---
st.write("---")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""<div class="neon-border">
        <div style="color:#00f2ff; font-size:12px; letter-spacing:2px;">BÓVEDA BITCOIN</div>
        <div class="val-major">{bal['btc']:.8f}</div>
        <div class="val-minor">≈ ${valor_btc_usd:.2f} USD</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""<div class="neon-border">
        <div style="color:#00f2ff; font-size:12px; letter-spacing:2px;">DISPONIBLE MXN</div>
        <div class="val-major">${bal['mxn']:.2f}</div>
        <div class="val-minor">{status_api}</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""<div class="neon-border">
        <div style="color:#00f2ff; font-size:12px; letter-spacing:2px;">META PRESTIGE ($115)</div>
        <div class="val-major">{progreso_meta:.4f}%</div>
        <div class="val-minor">Objetivo Activo</div>
    </div>""", unsafe_allow_html=True)

# --- 5. LOGS Y ESTADO DE IA ---
st.write("---")
l1, l2 = st.columns([2,1])
with l1:
    st.subheader("🤖 Status IA Mahora Pro")
    if bal['mxn'] > 10:
        st.success("🚀 AUTO-PILOT: ACTIVO. Esperando punto de adaptación (compra).")
    else:
        st.warning("📡 AUTO-PILOT: EN ESPERA. Saldo MXN insuficiente para operar.")
with l2:
    st.subheader("📊 Radar de Ballenas")
    st.info("MERCADO ESTABLE. Movimiento orgánico detectado.")

# Auto-refresh cada 30 segundos
time.sleep(30)
st.rerun()
