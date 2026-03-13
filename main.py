import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd

# --- CONFIGURACIÓN CORE ---
st.set_page_config(layout="wide", page_title="SHARK NEON v9.2")

# --- CREDENCIALES ---
API_KEY = st.secrets.get("BITSO_API_KEY", "").strip()
API_SECRET = st.secrets.get("BITSO_API_SECRET", "").strip()

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp { background-color: #020205; color: #00d4ff; }
    .card { background: #0a0a0f; border: 1px solid #bc13fe; padding: 20px; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

def bitso_auth_request(path):
    """Protocolo de firma v9.2 - Precisión absoluta"""
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + path
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    
    headers = {
        'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}',
        'Content-Type': 'application/json'
    }
    
    url = f"https://api.bitso.com{path}"
    return requests.get(url, headers=headers)

# --- LÓGICA DE DATOS ---
st.title("🦈 SHARK SYSTEM v9.2")
st.write(f"Protocolo: **Starship 2026** | Operador: **Pavo Free Fire**")

col_info, col_balance = st.columns([1, 2])

with col_info:
    st.subheader("📡 ESTADO DEL NODO")
    if not API_KEY:
        st.error("Faltan llaves en Secrets")
    else:
        response = bitso_auth_request("/v3/balances")
        if response.status_code == 200:
            st.success("🟢 CONEXIÓN ESTABLE")
            balances = response.json()['payload']['balances']
            status = "OK"
        else:
            status = "ERROR"
            st.error(f"Fallo: {response.status_code}")
            st.write(f"Detalle: {response.text}")
            st.info("💡 **TIP:** Si ves 404, la API Key 'SharkElite' aún no se propaga. Espera 2 min.")

with col_balance:
    st.subheader("🎯 META SUV $1.7M")
    # Meta de la camioneta de 1.7 millones
    meta_objetivo = 1700000
    saldo_total_mxn = 0.0
    
    if status == "OK":
        wallet_rows = []
        for b in balances:
            qty = float(b['total'])
            if qty > 0:
                coin = b['currency'].upper()
                # Precio simple para no saturar la API
                p_resp = requests.get(f"https://api.bitso.com/v3/ticker/?book={coin.lower()}_mxn").json()
                price = float(p_resp['payload']['last']) if 'payload' in p_resp else 1.0
                valor = qty * price
                saldo_total_mxn += valor
                wallet_rows.append({"Token": coin, "Saldo": qty, "Valor MXN": f"${valor:,.2f}"})
        
        st.dataframe(pd.DataFrame(wallet_rows), use_container_width=True)
        
        progreso = min(saldo_total_mxn / meta_objetivo, 1.0)
        st.metric("TOTAL EN CARTERA", f"${saldo_total_mxn:,.2f} MXN")
        st.progress(progreso)
        st.write(f"Llevas el **{progreso*100:.2f}%** de tu camioneta.")
    else:
        st.warning("Esperando conexión para calcular progreso...")
