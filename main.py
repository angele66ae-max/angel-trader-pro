import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hmac, hashlib, time, numpy as np
from datetime import datetime

# --- 1. CONFIGURACIÓN DE IDENTIDAD & HEADER (Reconstrucción Píxel) ---
NOMBRE_USUARIO = "Angel"
st.set_page_config(layout="wide", page_title=f"MahoraShark - {NOMBRE_USUARIO}'s Prestige", page_icon="⛩️")

# --- CONEXIÓN REAL BITSO & SEGURIDAD ---
API_KEY = st.secrets.get("BITSO_KEY")
API_SECRET = st.secrets.get("BITSO_SECRET")
MODO_REAL = True if API_KEY and API_SECRET else False

def firmar(metodo, endpoint, cuerpo=""):
    nonce = str(int(time.time() * 1000))
    mensaje = nonce + metodo + endpoint + cuerpo
    firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}

# --- 🎯 ESTILO VISUAL (Cyberpunk, Neón, Glow, Gotas) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"

st.markdown(f"""
    <style>
    /* Fondo Cósmico con Gotas */
    .stApp {{ 
        background: linear-gradient(rgba(5, 10, 14, 0.95), rgba(5, 10, 14, 0.98)), url("{fondo_url}"); 
        background-size: cover; background-attachment: fixed; color: white; 
    }}
    /* Header Principal con Glow Cyan */
    .main-header {{
        text-align: center; color: #ffffff; font-weight: bold; font-size: 36px;
        text-shadow: 0 0 15px #00f2ff, 0 0 25px #00f2ff; letter-spacing: 3px; padding: 15px;
        border-bottom: 2px solid #00f2ff; box-shadow: 0 5px 15px rgba(0, 242, 255, 0.3);
        margin-bottom: 20px;
    }}
    /* Tarjetas de Métricas Neón */
    .metric-card {{
        background: rgba(11, 20, 26, 0.9); border: 2px solid #00f2ff;
        border-radius: 10px; padding: 15px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
    }}
    .metric-title {{ font-size: 12px; color: #8b9bb4; text-transform: uppercase; letter-spacing: 1px; }}
    .metric-val {{ font-size: 26px; font-weight: bold; color: #00f2ff; text-shadow: 0 0 10px #00f2ff; }}
    /* Consola Cerebro Mahora (Estilo Hacker) */
    .ia-terminal {{
        background: rgba(0,0,0,0.9); border: 2px solid #ff00ff;
        border-radius: 10px; padding: 15px; font-family: 'Courier New', monospace;
        color: #39FF14; height: 350px; overflow-y: auto; box-shadow: 0 0 15px rgba(255, 0, 255, 0.2);
    }}
