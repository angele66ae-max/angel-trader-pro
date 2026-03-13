import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(
    page_title="Angel Trader PRO",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Angel Trader PRO")
st.subheader("Trading Dashboard BTC / MXN")

# -----------------------------
# FUNCION PARA OBTENER PRECIO
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
# PRECIO ACTUAL
# -----------------------------

precio = obtener_precio()

col1, col2 = st.columns(2)

with col1:
    if precio:
        st.success("Conectado a Bitso")
        st.metric(
            label="Precio BTC/MXN",
            value=f"${precio:,.2f}"
        )
    else:
        st.error("No se pudo conectar a Bitso")

with col2:
    st.metric(
        label="Estado del sistema",
        value="Activo"
    )

# -----------------------------
# GRAFICA DE PRECIO
# -----------------------------

st.subheader("📈 Movimiento del precio")

if "datos" not in st.session_state:
    st.session_state.datos = []

precio = obtener_precio()

if precio:
    st.session_state.datos.append(precio)

df = pd.DataFrame(st.session_state.datos, columns=["BTC"])

st.line_chart(df)

# -----------------------------
# SIMULADOR DE COMPRA
# -----------------------------

st.subheader("💰 Simulador de compra")

monto = st.number_input(
    "Cantidad MXN para comprar BTC",
    min_value=100,
    value=1000
)

if st.button("Comprar BTC (simulación)"):

    precio = obtener_precio()

    btc = monto / precio

    st.success("Compra simulada ejecutada")

    st.write(f"MXN usados: ${monto}")
    st.write(f"BTC recibidos: {btc:.6f}")

# -----------------------------
# AUTO REFRESH
# -----------------------------

time.sleep(3)
st.rerun()

# -----------------------------
# FOOTER
# -----------------------------

st.write("---")
st.caption("Angel Trader PRO | Sistema experimental de trading")
