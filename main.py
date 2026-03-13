import streamlit as st
import time, hashlib, hmac, json
import requests
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="SHARK NEON v9.8")

# --- CREDENCIALES ---
API_KEY = st.secrets.get("BITSO_API_KEY", "").strip()
API_SECRET = st.secrets.get("BITSO_API_SECRET", "").strip()

# --- ESTILO NEÓN ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00d4ff; }
    .neon-card { border: 1px solid #bc13fe; padding: 15px; border-radius: 10px; background: #111; box-shadow: 0 0 10px #bc13fe; }
    </style>
    """, unsafe_allow_html=True)

def bitso_ghost_call(path):
    """Protocolo Fantasma v9.8 - Salto de Firewalls"""
    nonce = str(int(time.time() * 1000))
    # Intentamos con el método POST a balances (algunas versiones de API lo aceptan para evitar el 404 de GET)
    message = nonce + "GET" + path
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    
    headers = {
        'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Bitso/v3 Python/3.14' # Camuflaje de User-Agent
    }
    
    # Probamos con la URL base alternativa
    url = f"https://api.bitso.com{path}"
    return requests.get(url, headers=headers, timeout=10)

def get_ticker(book):
    try:
        r = requests.get(f"https://api.bitso.com/v3/ticker/?book={book}").json()
        return float(r['payload']['last'])
    except: return 0.0

# --- LÓGICA DE INTERFAZ ---
st.title("🦈 SHARK SYSTEM v9.8")
st.write(f"Protocolo: **Ghost 2026** | Operador: **Pavo Free Fire**")

# MONITOR DE METAS
meta_suv = 1700000 # Tu meta de 1.7 millones
saldo_total = 0.0

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📡 ESTADO DEL NODO")
    if not API_KEY:
        st.error("Configura tus Secrets en Streamlit.")
    else:
        # Probamos el endpoint de balances pero sin la diagonal final
        r = bitso_ghost_call("/v3/balances")
        
        if r.status_code == 200:
            st.success("🟢 SISTEMA SINCRONIZADO")
            balances = r.json()['payload']['balances']
            status_ok = True
        else:
            status_ok = False
            st.markdown(f"""
            <div class="neon-card">
                <b style='color:#ff4b4b'>🔴 FALLO DE RUTA: {r.status_code}</b><br>
                Detalle: El servidor de Bitso sigue bloqueando la conexión desde Streamlit.
            </div>
            """, unsafe_allow_html=True)
            st.info("🚨 **SOLUCIÓN FINAL:** Si el 404 sigue, el problema es el 'Host' de Streamlit. Tendremos que usar un Proxy o cambiar la URL de la API.")

with col2:
    st.subheader("🎯 PROGRESO SUV ($1.7M)")
    if status_ok:
        datos_tabla = []
        for b in balances:
            qty = float(b['total'])
            if qty > 0:
                coin = b['currency'].upper()
                price = 1.0 if coin == "MXN" else get_ticker(f"{coin.lower()}_mxn")
                val_mxn = qty * price
                saldo_total += val_mxn
                datos_tabla.append({"Moneda": coin, "Balance": qty, "MXN": f"${val_mxn:,.2f}"})
        
        st.table(pd.DataFrame(datos_tabla))
        
        # Cálculo de meta SUV
        porcentaje = min(saldo_total / meta_suv, 1.0)
        st.metric("SALDO TOTAL", f"${saldo_total:,.2f} MXN")
        st.progress(porcentaje)
        st.write(f"Faltan **${(meta_suv - saldo_total):,.2f} MXN** para tu camioneta.")
    else:
        st.warning("Esperando datos de Bitso para calcular progreso...")

# TICKERS EN TIEMPO REAL
st.divider()
t1, t2, t3 = st.columns(3)
t1.metric("₿ BTC", f"${get_ticker('btc_mxn'):,.0f} MXN")
t2.metric("Ξ ETH", f"${get_ticker('eth_mxn'):,.0f} MXN")
t3.metric("💵 USD", f"${get_ticker('usd_mxn'):,.2f} MXN")
