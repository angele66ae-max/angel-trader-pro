import streamlit as st
import time, hashlib, hmac, json
import pandas as pd
import urllib3 # Librería de bajo nivel para máxima estabilidad

# --- CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="SHARK NEON v9.5")

# --- CREDENCIALES ---
API_KEY = st.secrets.get("BITSO_API_KEY", "").strip()
API_SECRET = st.secrets.get("BITSO_API_SECRET", "").strip()

# --- ESTILO SHARK ---
st.markdown("""
    <style>
    .stApp { background-color: #010103; color: #00d4ff; }
    .status-panel { border: 2px solid #bc13fe; padding: 20px; border-radius: 15px; background: #0a0a0f; }
    </style>
    """, unsafe_allow_html=True)

def bitso_wallbreaker(path):
    """Protocolo de Conexión de Bajo Nivel v9.5"""
    http = urllib3.PoolManager()
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + path
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    
    headers = {
        'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (SharkSystem/9.5)'
    }
    
    # Forzamos la URL sin barras diagonales dobles al final
    url = f"https://api.bitso.com{path.rstrip('/')}"
    return http.request('GET', url, headers=headers)

def get_ticker_lite(book):
    try:
        r = urllib3.PoolManager().request('GET', f"https://api.bitso.com/v3/ticker/?book={book}")
        data = json.loads(r.data.decode('utf-8'))
        return float(data['payload']['last'])
    except: return 0.0

# --- INTERFAZ PRINCIPAL ---
st.title("🦈 SHARK SYSTEM v9.5")
st.write(f"Operador: **Pavo Free Fire** | Status Meta: **SUV 1.7M**")

col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("📡 CONEXIÓN AL NODO")
    if not API_KEY or not API_SECRET:
        st.error("⚠️ Error: Configura tus Secrets.")
    else:
        resp = bitso_wallbreaker("/v3/balances")
        if resp.status == 200:
            st.success("🟢 SISTEMA ONLINE")
            balances = json.loads(resp.data.decode('utf-8'))['payload']['balances']
            con_exito = True
        else:
            con_exito = False
            st.markdown(f"""
            <div class="status-panel">
                <h4 style='color:#ff4b4b'>🔴 FALLO CRÍTICO</h4>
                <b>Código:</b> {resp.status}<br>
                <b>Mensaje:</b> Acceso denegado por Bitso.
            </div>
            """, unsafe_allow_html=True)
            st.info("💡 **SOLUCIÓN MAESTRA:** Si el 404 persiste, entra a Bitso > Perfil > Seguridad y desactiva cualquier opción de 'Restricción por IP' global.")

with col_right:
    # META DE LA CAMIONETA 1.7M
    meta = 1700000
    total_mxn = 0.0
    
    if con_exito:
        wallet_list = []
        for b in balances:
            qty = float(b['total'])
            if qty > 0:
                coin = b['currency'].upper()
                price = 1.0 if coin == "MXN" else get_ticker_lite(f"{coin.lower()}_mxn")
                sub = qty * price
                total_mxn += sub
                wallet_list.append({"Token": coin, "Balance": qty, "Valor MXN": f"${sub:,.2f}"})
        
        st.dataframe(pd.DataFrame(wallet_list), hide_index=True)
        
        progreso = min(total_mxn / meta, 1.0)
        st.metric("CAPITAL TOTAL", f"${total_mxn:,.2f} MXN")
        st.write(f"🚀 **Avance para la SUV:** {progreso*100:.2f}%")
        st.progress(progreso)
    else:
        st.warning("Esperando datos para actualizar meta de 1.7M...")

# --- TICKERS ---
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("₿ BTC", f"${get_ticker_lite('btc_mxn'):,.0f}")
c2.metric("Ξ ETH", f"${get_ticker_lite('eth_mxn'):,.0f}")
c3.metric("💵 USD", f"${get_ticker_lite('usd_mxn'):,.2f}")
