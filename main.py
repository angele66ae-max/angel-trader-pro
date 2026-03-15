import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import hmac
import hashlib
import json
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN CORE ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE", initial_sidebar_state="collapsed")

# --- 1. LLAVES DE PRODUCCIÓN SINCRONIZADAS ---
BITSO_API_KEY = "FZHAAOqOhy"
BITSO_API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

# --- ESTILO VISUAL PRESTIGE ---
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{FONDO_URL}");
        background-size: cover; background-attachment: fixed;
    }}
    .card {{
        background: rgba(0, 10, 20, 0.9);
        border: 2px solid #00f2ff;
        border-radius: 12px; padding: 20px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
    }}
    .metric-val {{ font-size: 32px; color: #00f2ff; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }}
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE OPERACIONES REALES ---
def execute_bitso_action(side, amount_usd):
    nonce = str(int(time.time() * 1000))
    path = "/v3/orders/"
    # Definimos la orden de mercado en el libro btc_usd
    payload = {
