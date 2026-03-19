import streamlit as st
import requests
import pandas as pd

# Conexión simple a Bitso
def obtener_bitso():
    url = "https://api.bitso.com/v3/ticker/?book=btc_mxn"
    response = requests.get(url).json()
    return float(response['payload']['last'])

precio = obtener_bitso()
st.metric("BTC en Bitso (MXN)", f"${precio:,.2f}")
st.write(f"Objetivo: $115.00")
