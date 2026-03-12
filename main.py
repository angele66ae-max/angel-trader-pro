import streamlit as st
import time, requests, hashlib, hmac, os

# --- CONFIGURACIÓN DE SEGURIDAD ---
API_KEY = st.secrets.get("BITSO_API_KEY")
API_SECRET = st.secrets.get("BITSO_API_SECRET")

st.set_page_config(layout="wide", page_title="ANGEL IA | DEBUG MODE")

# Estilo Neón
st.markdown("<style>.stApp { background: #05000a; color: #bc00ff; }</style>", unsafe_allow_html=True)

class AngelEngine:
    def __init__(self):
        self.base = "https://api.bitso.com/v3"

    def get_balances(self):
        # --- PROCESO DE FIRMA OFICIAL DE BITSO ---
        path = "/v3/balances/"
        method = "GET"
        nonce = str(int(time.time() * 1000))
        message = nonce + method + path
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
        
        headers = {
            'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}',
            'Content-Type': 'application/json'
        }
        
        try:
            r = requests.get(f"https://api.bitso.com{path}", headers=headers)
            data = r.json()
            if r.status_code != 200:
                return None, f"⚠️ Error de Bitso: {data['error']['message']}"
            return data['payload']['balances'], "OK"
        except Exception as e:
            return None, f"⚠️ Error de Conexión: {str(e)}"

    def get_ticker(self, book):
        try:
            r = requests.get(f"{self.base}/ticker/?book={book}").json()
            return float(r['payload']['last'])
        except: return 0.0

bot = AngelEngine()
st.title("💜 DIAGNÓSTICO DE CARTERA 💜")

# Ejecutar Diagnóstico
saldos, status = bot.get_balances()
p_usd = bot.get_ticker("usd_mxn") or 18.0

if status != "OK":
    st.error(status)
    st.info("💡 Tip: Revisa que tus API Keys en Streamlit Secrets no tengan espacios extra y que tengan permisos de 'Balances' en Bitso.")
else:
    st.success("✅ Conexión Exitosa con Bitso")
    total_cartera = 0.0
    for s in saldos:
        cantidad = float(s['total'])
        if cantidad > 0:
            moneda = s['currency'].upper()
            # Calcular valor
            if moneda == 'MXN': p = 1.0
            else: 
                p = bot.get_ticker(f"{moneda.lower()}_mxn")
                if p == 0: p = bot.get_ticker(f"{moneda.lower()}_usd") * p_usd
            
            valor_mxn = cantidad * p
            total_cartera += valor_mxn
            st.write(f"💎 {moneda}: {cantidad} (~${valor_mxn:,.2f} MXN)")

    st.divider()
    st.metric("SALDO TOTAL REAL", f"${total_cartera:,.2f} MXN")
    
    meta_mxn = 10000 * p_usd
    progreso = min(total_cartera / meta_mxn, 1.0)
    st.progress(progreso)
    st.write(f"Progreso a la meta: {progreso*100:.4f}%")
