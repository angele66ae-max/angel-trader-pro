import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- LECTURA LIMPIA DE CREDENCIALES ---
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

st.set_page_config(layout="wide", page_title="SHARK TANK | LIVE")

# Estilo TradingView Dark
st.markdown("""
    <style>
    .stApp { background: #0b0e14; color: #d1d4dc; }
    .stMetric { background: #161a25; border: 1px solid #2a2e39; border-radius: 8px; }
    h1, h2 { color: #2962ff !important; }
    .wallet-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

class SharkEngine:
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.base_url = "https://api.bitso.com"

    def get_price(self, book):
        try:
            r = requests.get(f"{self.base_url}/v3/ticker/?book={book}", timeout=5).json()
            return float(r['payload']['last'])
        except: return 0.0

    def get_balances(self):
        if not self.key or not self.secret:
            return None, "Faltan credenciales en Secrets"
        
        path = "/v3/balances/"
        # Usamos un nonce ligeramente desplazado para evitar errores de sincronización
        nonce = str(int(time.time() * 1000))
        message = nonce + "GET" + path
        
        signature = hmac.new(
            self.secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        auth_header = f"Bitso {self.key}:{nonce}:{signature}"
        
        try:
            r = requests.get(
                self.base_url + path, 
                headers={'Authorization': auth_header},
                timeout=10
            )
            data = r.json()
            if r.status_code == 200:
                return data['payload']['balances'], "OK"
            else:
                # Captura el mensaje real de Bitso
                error_msg = data.get('error', {}).get('message', 'Error desconocido')
                return None, f"Bitso dice: {error_msg}"
        except Exception as e:
            return None, f"Error de sistema: {str(e)}"

bot = SharkEngine(API_KEY, API_SECRET)
st.title("🦈 SHARK TANK: PORTFOLIO DASHBOARD")

# --- RESUMEN DE MERCADO ---
p_usd = bot.get_price("usd_mxn") or 18.25
assets = ["btc_mxn", "eth_mxn", "usd_mxn"]
cols = st.columns(len(assets))
for i, asset in enumerate(assets):
    cols[i].metric(asset.split('_')[0].upper(), f"${bot.get_price(asset):,.2f} MXN")

st.divider()

# --- BILLETERA DETALLADA (Lo que pediste) ---
st.header("💰 Mi Billetera Crypto")
balances, status = bot.get_balances()
total_mxn = 0.0

if status == "OK":
    wallet_data = []
    for b in balances:
        cantidad = float(b['total'])
        if cantidad > 0:
            coin = b['currency'].upper()
            # Obtener precio de conversión
            if coin == 'MXN': p_actual = 1.0
            else:
                p_actual = bot.get_price(f"{coin.lower()}_mxn")
                if p_actual == 0: p_actual = bot.get_price(f"{coin.lower()}_usd") * p_usd
            
            valor_mxn = cantidad * p_actual
            valor_usd = valor_mxn / p_usd
            total_mxn += valor_mxn
            
            if valor_mxn > 0.01: # Solo mostrar si vale más de 1 centavo
                wallet_data.append({
                    "MONEDA": coin,
                    "SALDO CRYPTO": f"{cantidad:.8f}",
                    "VALOR EN PESOS": f"${valor_mxn:,.2f} MXN",
                    "VALOR EN DÓLARES": f"${valor_usd:,.2f} USD"
                })
    
    if wallet_data:
        st.table(pd.DataFrame(wallet_data))
        
        # Métricas Globales
        c1, c2, c3 = st.columns(3)
        c1.metric("VALOR TOTAL (MXN)", f"${total_mxn:,.2f}")
        c2.metric("VALOR TOTAL (USD)", f"${(total_mxn/p_usd):,.2f}")
        
        progreso = min((total_mxn/p_usd) / 10000, 1.0)
        c3.metric("META $10K USD", f"{progreso*100:.4f}%")
        st.progress(progreso)
    else:
        st.info("Billetera vacía o saldos demasiado pequeños para mostrar.")
else:
    st.error(f"❌ ERROR: {status}")
    st.info("Revisa que tu API Key en Bitso tenga activado: 'Consultar saldos'.")

# --- GRÁFICA ESTILO TRADINGVIEW ---
st.divider()
st.subheader("📈 Gráfica de Análisis")
p_btc = bot.get_price("btc_mxn") or 1230000
df = pd.DataFrame({'Open': [p_btc]*15, 'High': [p_btc*1.001]*15, 'Low': [p_btc*0.999]*15, 'Close': [p_btc]*15, 'Volume': [100]*15})
df.index = pd.date_range(start=datetime.now(), periods=15, freq='15min')
mc = mpf.make_marketcolors(up='#26a69a', down='#ef5350', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#2a2e39', facecolor='#0b0e14', edgecolor='#2a2e39')
buf = BytesIO(); mpf.plot(df, type='candle', style=s, figratio=(16,6), savefig=dict(fname=buf, dpi=100))
st.image(buf, use_container_width=True)
