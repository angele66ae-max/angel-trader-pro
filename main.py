import streamlit as st
import requests
import pandas as pd
import time

# -------------------------------
# CONFIGURACIÓN DE LA APP
# -------------------------------

st.set_page_config(
    page_title="Angel Trader PRO",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Angel Trader PRO")
st.subheader("Trading Dashboard BTC / MXN")

# -------------------------------
# FUNCION PARA OBTENER PRECIO
# -------------------------------

def obtener_precio():
    url = "https://api.bitso.com/v3/ticker/?book=btc_mxn"

    try:
        response = requests.get(url)
        data = response.json()

        precio = float(data["payload"]["last"])
        return precio

    except:
        return None


# -------------------------------
# PANEL PRINCIPAL
# -------------------------------

precio = obtener_precio()

if precio:

    st.success("Conectado a Bitso")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Precio BTC/MXN",
            value=f"${precio:,.2f}"
        )

    with col2:
        st.metric(
            label="Estado",
            value="Activo"
        )

else:

    st.error("❌ No se pudo obtener el precio")

# -------------------------------
# GRAFICA SIMPLE
# -------------------------------

st.subheader("📈 Movimiento del precio")

precios = []

for i in range(10):

    precio = obtener_precio()

    if precio:
        precios.append(precio)

    time.sleep(1)

df = pd.DataFrame(precios, columns=["BTC"])

st.line_chart(df)

# -------------------------------
# SIMULADOR DE COMPRA
# -------------------------------

st.subheader("💰 Simulador de compra")

monto = st.number_input(
    "Cantidad MXN para comprar BTC",
    min_value=100,
    value=100
)

if st.button("Comprar BTC (simulación)"):

    precio = obtener_precio()

    btc = monto / precio

    st.success(f"Compra simulada:")
    st.write(f"MXN usados: ${monto}")
    st.write(f"BTC recibidos: {btc:.6f}")

# -------------------------------
# FOOTER
# -------------------------------

st.write("---")

st.caption("Angel Trader PRO | Sistema de trading experimental")
