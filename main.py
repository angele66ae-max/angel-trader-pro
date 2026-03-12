import streamlit as st
import time, requests, hashlib, hmac, pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CONFIGURACIÓN DE SEGURIDAD ---
API_KEY = st.secrets.get("BITSO_API_KEY", "").strip()
API_SECRET = st.secrets.get("BITSO_API_SECRET", "").strip()

st.set_page_config(layout="wide", page_title="SHARK TANK | CRYPTO PORTFOLIO")

# Estilo Dark Pro
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #e0e0e0; }
    .crypto-card { background: #1c2128; border: 1px solid #30363d; border-radius: 10px; padding: 15px; margin-bottom: 10px; }
    .price-up { color: #26a69a; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

class SharkEngine:
    def __init__(self):
        self.base = "https://api.bitso.com"

    def get_price(self, book):
        try:
            r = requests.get(f"{self.base}/v3/ticker/?book={book}").json()
            return float(r['payload']['last'])
        except: return 0.0

    def get_balances(self):
        if not API_KEY or not API_SECRET: return None, "Faltan API Keys"
        nonce = str(int(time.time() * 1000))
        path = "/v3/balances/"
        msg = nonce + "GET" + path
        signature = hmac.new(API_SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
        try:
            r = requests.get(self.base + path, headers=headers, timeout=10)
            res = r.json()
            return (res['payload']['balances'], "OK") if r.status_code == 200 else (None, res['error']['message'])
        except Exception as e: return None, str(e)

bot = SharkEngine()
p_usd_mxn = bot.get_price("usd_mxn") or 18.10  # Precio del dólar hoy

st.title("🦈 ANGEL IA: DASHBOARD DE INVERSIÓN")

# 1. MERCADO EN VIVO
st.subheader("📊 Monitor de Mercado")
assets = ["btc_mxn", "eth_mxn", "usd_mxn"]
cols = st.columns(3)
for i, a in enumerate(assets):
    price = bot.get_price(a)
    cols[i].metric(a.upper().replace("_MXN", ""), f"${price:,.2f} MXN")

st.divider()

# 2. NUEVO APARTADO: MI BILLETERA CRYPTO
col_main, col_side = st.columns([2, 1])

with col_main:
    st.subheader("💰 Mi Billetera Crypto")
    balances, status = bot.get_balances()
    total_mxn_wallet = 0.0

    if status == "OK":
        # Crear una tabla para organizar la info
        crypto_data = []
        for b in balances:
            qty = float(b['total'])
            if qty > 0.000001: # Solo mostrar lo que tiene saldo
                coin = b['currency'].upper()
                # Calcular valor en MXN
                if coin == 'MXN': p_mxn = 1.0
                else:
                    p_mxn = bot.get_price(f"{coin.lower()}_mxn")
                    if p_mxn == 0: p_mxn = bot.get_price(f"{coin.lower()}_usd") * p_usd_mxn
                
                val_mxn = qty * p_mxn
                val_usd = val_mxn / p_usd_mxn
                total_mxn_wallet += val_mxn
                
                crypto_data.append({
                    "Moneda": coin,
                    "Cantidad": f"{qty:.8f}",
                    "Valor MXN": f"${val_mxn:,.2e}",
                    "Valor USD": f"${val_usd:,.2f}"
                })
        
        if crypto_data:
            st.table(pd.DataFrame(crypto_data))
        else:
            st.warning("No se detectaron monedas con saldo mayor a cero.")
    else:
        st.error(f"Error de conexión: {status}")
        st.info("Tip: Revisa que tus API Keys tengan permiso de 'Balances' en Bitso.")

with col_side:
    st.subheader("🎯 Resumen Total")
    st.metric("SALDO TOTAL (MXN)", f"${total_mxn_wallet:,.2f}")
    st.metric("SALDO TOTAL (USD)", f"${(total_mxn_wallet / p_usd_mxn):,.2f}")
    
    # Progreso Meta
    meta_mxn = 177570.0  # Los $10k USD de tu meta
    progreso = min(total_mxn_wallet / meta_mxn, 1.0)
    st.write(f"**Progreso hacia Meta:** {progreso*100:.4f}%")
    st.progress(progreso)
