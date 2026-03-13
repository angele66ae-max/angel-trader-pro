import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

st.set_page_config(
    page_title="Angel Trader PRO",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# ESTILO PROFESIONAL
# -----------------------------

st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.metric-container {
    background-color: #111827;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Angel Trader PRO")
st.caption("Plataforma experimental de trading")

# -----------------------------
# API BITSO
# -----------------------------

def obtener_precio():
    url = "https://api.bitso.com/v3/ticker/?book=btc_mxn"

    try:
        r = requests.get(url)
        data = r.json()
        precio = float(data["payload"]["last"])
        return precio
    except:
        return None

# -----------------------------
# PANEL PRINCIPAL
# -----------------------------

precio = obtener_precio()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="BTC/MXN",
        value=f"${precio:,.2f}"
    )

with col2:
    st.metric(
        label="Estado",
        value="Conectado"
    )

with col3:
    st.metric(
        label="Servidor",
        value="Activo"
    )

# -----------------------------
# HISTORIAL DE PRECIOS
# -----------------------------

if "precios" not in st.session_state:
    st.session_state.precios = []

if precio:
    st.session_state.precios.append(precio)

# limitar datos
if len(st.session_state.precios) > 50:
    st.session_state.precios.pop(0)

df = pd.DataFrame(st.session_state.precios, columns=["precio"])

# -----------------------------
# GRAFICA PRO
# -----------------------------

st.subheader("📈 Gráfica del mercado")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        y=df["precio"],
        mode="lines",
        line=dict(color="#00ffcc", width=3),
        name="BTC"
    )
)

fig.update_layout(
    template="plotly_dark",
    height=500,
    margin=dict(l=10, r=10, t=30, b=10)
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# SIMULADOR
# -----------------------------

st.subheader("💰 Simulación de compra")

monto = st.number_input(
    "Cantidad MXN",
    min_value=100,
    value=1000
)

if st.button("Comprar BTC"):

    btc = monto / precio

    st.success("Compra simulada")

    st.write(f"MXN usados: ${monto}")
    st.write(f"BTC recibidos: {btc:.6f}")

# -----------------------------
# ACTUALIZAR AUTOMATICAMENTE
# -----------------------------

time.sleep(2)
st.rerun()
