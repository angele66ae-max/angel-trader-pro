import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
import hmac
import hashlib
from datetime import datetime
import plotly.graph_objects as go

# ---------- CONFIGURACIÓN DE PÁGINA ----------
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

# URL Directa de la imagen (Asegúrate de que el enlace sea público)
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

# ---------- ESTILO CSS (FIX DE FONDO Y TRANSPARENCIA) ----------
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("{FONDO_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .card {{
        background: rgba(10, 10, 15, 0.85);
        border: 1px solid #00f2ff;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
    }}
    .metric-val {{
        font-size: 32px;
        color: #00f2ff;
        font-weight: bold;
        text-shadow: 0 0 8px #00f2ff;
    }}
</style>
""", unsafe_allow_html=True)

# ---------- FUNCIONES DE BITSO (CORREGIDAS) ----------
def get_bitso_ticker():
    try:
        # Usamos requests directo para evitar fallos de ccxt
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd", timeout=5)
        data = r.json()
        return float(data['payload']['last'])
    except:
        return 71500.0 # Valor fallback si falla la red

# ---------- LÓGICA DE DATOS ----------
if "precios" not in st.session_state:
    st.session_state.precios = []

current_price = get_bitso_ticker()
st.session_state.precios.append(current_price)
if len(st.session_state.precios) > 40: st.session_state.precios.pop(0)

# ---------- INTERFAZ DASHBOARD ----------
st.markdown("<h
