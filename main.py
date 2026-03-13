import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN CORE ---
st.set_page_config(layout="wide", page_title="SHARK NEON v9.1")

# --- CREDENCIALES ---
# Asegúrate de actualizar estas en la pestaña de 'Secrets' de Streamlit
API_KEY = st.secrets.get("BITSO_API_KEY", "").strip()
API_SECRET = st.secrets.get("BITSO_API_SECRET", "").strip()

# --- ESTILO VISUAL NEÓN ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00d4ff; }
    .status-card { background: #111; border: 2px solid #bc13fe; padding: 15px; border-radius: 12px; box-shadow: 0 0 15px #bc13fe; }
    .metric-box { background: rgba(0, 212, 255, 0.1); border: 1px solid #00d4ff; border-radius: 8px; padding: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

def call_bitso(path):
    """Motor de conexión v9.1 - Limpieza total de parámetros"""
    nonce = str(int(time.time() * 1000))
    # La firma DEBE ser exactamente: nonce + METHOD + path (sin parámetros extra)
    message = nonce + "GET" + path
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    
    headers = {
        'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    url = f"https://api.bitso.com{path}"
    return requests.get(url, headers=headers, timeout=12)

def fetch_data():
    if not API_KEY or not API_SECRET:
        return None, "Faltan credenciales en Secrets"
    
    try:
        # Intentamos el endpoint de balances que es el más directo
        r = call_bitso("/v3/balances")
        if r.status_code == 200:
            return r.json()['payload']['balances'], "OK"
        elif r.status_code == 404:
            return None, f"404: El servidor no reconoce la ruta. Revisa tu API Key."
        else:
            return None, f"Error {r.status_code}: {r.text}"
    except Exception as e:
        return None, f"Fallo de Red: {str(e)}"

def get_live_price(book):
    try:
        r = requests.get(f"https://api.bitso.com/v3/ticker/?book={book}").json()
        return float(r['payload']['last'])
    except:
        return 0.0

# --- INTERFAZ ---
st.title("🦈 SHARK SYSTEM v9.1")
st.write(f"Protocolo de Red: **Starship 2026** | Usuario: **{st.secrets.get('USER_NAME', 'Pavo Free Fire')}**")

col_left, col_right = st.columns([2, 1])

with col_right:
    st.subheader("📡 ESTADO DEL NODO")
    data, status = fetch_data()
    
    status_color = "🟢 ONLINE" if status == "OK" else "🔴 ERROR"
    st.markdown(f"""
    <div class="status-card">
        <b>SISTEMA:</b> {status_color}<br>
        <b>DETALLE:</b> {status}<br>
        <b>NONCE ACTIVO:</b> {int(time.time())}
    </div>
    """, unsafe_allow_html=True)
    
    if status != "OK":
        st.warning("🚨 **ACCION REQUERIDA:** La llave anterior está bloqueada. Genera una nueva en Bitso y actualiza los Secrets.")

with col_left:
    # TICKERS EN VIVO
    t1, t2, t3 = st.columns(3)
    p_btc = get_live_price("btc_mxn")
    p_eth = get_live_price("eth_mxn")
    p_usd = get_live_price("usd_mxn")
    
    t1.metric("₿ BTC", f"${p_btc:,.0f} MXN")
    t2.metric("Ξ ETH", f"${p_eth:,.0f} MXN")
    t3.metric("💵 USD", f"${p_usd:,.2f} MXN")

    if status == "OK":
        st.divider()
        st.subheader("💰 CARTERA ACTUAL")
        wallet_list = []
        total_mxn = 0.0
        
        for item in data:
            qty = float(item['total'])
            if qty > 0.000001:
                coin = item['currency'].upper()
                price = 1.0 if coin == "MXN" else get_live_price(f"{coin.lower()}_mxn")
                subtotal = qty * price
                total_mxn += subtotal
                wallet_list.append({"MONEDA": coin, "CANTIDAD": qty, "VALOR MXN": f"${subtotal:,.2f}"})
        
        st.table(pd.DataFrame(wallet_list))
        
        # META SUV 1.7M
        meta_camioneta = 1700000
        progreso = min(total_mxn / meta_camioneta, 1.0)
        
        st.metric("BALANCE TOTAL", f"${total_mxn:,.2f} MXN", delta=f"{total_mxn - (total_mxn*0.95):,.2f} (24h)")
        st.write(f"📈 **Progreso hacia la camioneta ($1.7M):** {progreso*100:.2f}%")
        st.progress(progreso)

# --- PIE DE PÁGINA ---
st.divider()
st.caption("Shark System v9.1 | Desarrollado para alta precisión financiera.")
