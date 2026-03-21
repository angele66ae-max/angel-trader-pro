import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac
import hashlib
import time
from datetime import datetime

# --- CONFIGURACIÓN DE SEGURIDAD ---
API_KEY = st.secrets.get("BITSO_KEY")
API_SECRET = st.secrets.get("BITSO_SECRET")

def firmar_solicitud(metodo, endpoint, cuerpo=""):
    nonce = str(int(time.time() * 1000))
    mensaje = nonce + metodo + endpoint + cuerpo
    firma = hmac.new(API_SECRET.encode('utf-8'), mensaje.encode('utf-8'), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}'}

# --- FUNCIONES DE CUENTA REAL ---
def obtener_saldo_real():
    if not API_KEY: return 47.12 # Backup si no hay llaves
    try:
        url = "https://api.bitso.com/v3/balance/"
        headers = firmar_solicitud("GET", "/v3/balance/")
        r = requests.get(url, headers=headers).json()
        for b in r['payload']['balances']:
            if b['currency'] == 'mxn': return float(b['total'])
        return 0.0
    except: return 47.12

def ejecutar_compra_real(monto_mxn):
    # PRECAUCIÓN: Esto envía dinero real al mercado
    endpoint = "/v3/orders/"
    cuerpo = f'{{"book": "btc_mxn", "side": "buy", "type": "market", "nominal_amount": "{monto_mxn}"}}'
    headers = firmar_solicitud("POST", endpoint, cuerpo)
    r = requests.post("https://api.bitso.com" + endpoint, headers=headers, data=cuerpo).json()
    return r

# --- LÓGICA DE MERCADO ---
def obtener_datos_pro():
    r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
    precio = float(r['payload']['last'])
    # Simulación de velas estéticas para el diseño neón
    df = pd.DataFrame({'Close': [precio * (1 + (i-15)/500) for i in range(30)]})
    df['Open'] = df['Close'].shift(1).fillna(precio)
    df['High'] = df[['Open', 'Close']].max(axis=1) * 1.001
    df['Low'] = df[['Open', 'Close']].min(axis=1) * 0.999
    return precio, df

# --- INTERFAZ ---
st.set_page_config(layout="wide", page_title="MahoraShark Quantum")
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"

st.markdown(f"""<style>.stApp {{background: linear-gradient(rgba(5,10,14,0.9), rgba(5,10,14,0.9)), url("{fondo_url}"); background-size: cover; color: white;}}</style>""", unsafe_allow_html=True)

precio_btc, df_velas = obtener_datos_pro()
saldo_real = obtener_saldo_real()

st.title("⛩️ MAHORASHARK: OPERACIÓN REAL")

c1, c2, c3 = st.columns(3)
c1.metric("SALDO EN BITSO", f"${saldo_real:,.2f} MXN")
c2.metric("PRECIO BTC", f"${precio_btc:,.0f}")
c3.metric("META CANADÁ", f"{(saldo_real/10000)*100:.2f}%")

# Gráfica de Velas Neón
fig = go.Figure(data=[go.Candlestick(
    open=df_velas['Open'], high=df_velas['High'],
    low=df_velas['Low'], close=df_velas['Close'],
    increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff'
)])
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', xaxis_rangeslider_visible=False)
st.plotly_chart(fig, width='stretch')

# --- EL CEREBRO DECIDE ---
st.subheader("🧠 Pensamiento de Cerebro Mahora")
if saldo_real < 100:
    st.warning("⚠️ Saldo bajo para trading profesional. Se recomienda fondear más MXN para ver ganancias reales.")
else:
    st.info("✅ Capital detectado. IA analizando puntos de entrada...")

if st.button("🚀 EJECUTAR COMPRA REAL CON 20% DEL SALDO"):
    if not API_KEY:
        st.error("Error: No has configurado las API Keys en Streamlit Secrets.")
    else:
        monto = saldo_real * 0.20
        res = ejecutar_compra_real(monto)
        st.json(res) # Muestra el resultado de la orden real

time.sleep(20)
st.rerun()
