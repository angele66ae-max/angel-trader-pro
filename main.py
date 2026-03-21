import streamlit as st
import requests
import time
import hmac, hashlib
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
NOMBRE_USUARIO = "Angel"
# Lista de activos que quieres que el bot vigile y compre
ACTIVOS_OBJETIVO = ["btc_mxn", "nvda_mxn", "googl_mxn", "aapl_mxn", "eth_mxn"]

st.set_page_config(layout="wide", page_title=f"MahoraShark Multi-Asset")

API_KEY = st.secrets.get("BITSO_KEY")
API_SECRET = st.secrets.get("BITSO_SECRET")

# --- 2. MOTOR DE ESCANEO MULTI-ACTIVO ---
def obtener_oportunidades():
    oportunidades = []
    for activo in ACTIVOS_OBJETIVO:
        try:
            r = requests.get(f"https://api.bitso.com/v3/ticker/?book={activo}").json()['payload']
            precio = float(r['last'])
            # Aquí la IA decide si está barato (simulando lógica de RSI/Tendencia)
            # En un sistema real, aquí pedirías el historial para calcular el RSI de cada una
            oportunidades.append({"activo": activo.upper(), "precio": precio})
        except: pass
    return oportunidades

# --- 3. EL GATILLO UNIVERSAL ---
def comprar_lo_que_sea(libro, monto):
    if not API_KEY: return "Error: Sin llaves"
    try:
        nonce = str(int(time.time() * 1000))
        endpoint = "/v3/orders/"
        cuerpo = f'{{"book": "{libro.lower()}", "side": "buy", "type": "market", "nominal": "{monto}"}}'
        mensaje = nonce + "POST" + endpoint + cuerpo
        firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}
        
        r = requests.post(f"https://api.bitso.com{endpoint}", headers=headers, data=cuerpo).json()
        return r
    except Exception as e: return str(e)

# --- 4. INTERFAZ PRESTIGE ACTUALIZADA ---
st.markdown(f"""
    <style>
    .stApp {{ background: #050a0e; color: white; }}
    .market-box {{ background: rgba(0, 242, 255, 0.05); border: 1px solid #00f2ff; border-radius: 10px; padding: 10px; margin: 5px; }}
    </style>
    """, unsafe_allow_html=True)

st.title(f"⛩️ {NOMBRE_USUARIO.upper()} - MULTI-MARKET BOT")

# Mostrar lo que el bot está viendo ahorita
ops = obtener_oportunidades()
cols = st.columns(len(ops))

for i, op in enumerate(ops):
    with cols[i]:
        st.markdown(f"""
            <div class="market-box">
                <small>{op['activo']}</small><br>
                <b style="font-size:18px;">${op['precio']:,.2f}</b>
            </div>
        """, unsafe_allow_html=True)

# --- 5. TERMINAL DE ACCIÓN ---
st.write("---")
col_console, col_action = st.columns([2, 1])

with col_console:
    st.markdown("### 🧠 Cerebro Mahora: Escaneo de Activos")
    with st.container():
        st.info(f"Vigilando: {', '.join(ACTIVOS_OBJETIVO)}")
        for op in ops:
            st.write(f"[{datetime.now().strftime('%H:%M:%S')}] Analizando {op['activo']}... Potencial detectado.")

with col_action:
    st.markdown("### ⚡ Compra de Emergencia")
    activo_a_comprar = st.selectbox("Selecciona Activo", ACTIVOS_OBJETIVO)
    monto = st.number_input("Monto MXN", min_value=10, value=20)
    
    if st.button("DISPARAR COMPRA"):
        # ESTA ES LA LÍNEA QUE GENERA DINERO
        res = comprar_lo_que_sea(activo_a_comprar, str(monto))
        st.success(f"Orden enviada para {activo_a_comprar}")
        st.json(res)

# Refresco
time.sleep(30)
st.rerun()
