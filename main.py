import streamlit as st
import plotly.graph_objects as go
import requests
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN DEL SISTEMA ---
SALDO_REAL = 144.95
FACTOR = 32
ASSET_NAME = "RENDER (IA)"

st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA V45")

# --- 2. DESIGN SYSTEM (CSS TÁCTICO) ---
st.markdown("""
<style>
    /* Fondo Dark Mode Profundo #0A0E14 */
    [data-testid="stHeader"], [data-testid="stToolbar"] {display: none !important;}
    .stApp { background-color: #0A0E14 !important; color: #00F2FF !important; font-family: 'Inter', sans-serif; }
    
    /* Header Estilo Guadaña */
    .header-box {
        display: flex; justify-content: space-between; align-items: center;
        background-color: #000; padding: 10px 20px; border-bottom: 2px solid #00F2FF;
    }
    .balance-val { font-size: 36px; color: #00FF00; font-weight: 700; text-shadow: 0 0 15px #00FF00; }
    .status-badge { background: #1a2a1a; color: #00FF00; border: 1px solid #00FF00; padding: 2px 8px; border-radius: 3px; font-size: 10px; font-weight: bold; margin-left: 5px; }

    /* Paneles Técnicos */
    .panel { border: 1px solid #00F2FF33; background: #0A0E14; padding: 15px; border-radius: 4px; }
    .label-min { font-size: 10px; color: #444 !important; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Terminal logs */
    .terminal { font-family: 'Consolas', monospace; font-size: 10px; color: #00F2FF; line-height: 1.2; }
    .ok { color: #00FF00; font-weight: bold; }

    /* Rueda de Mahoraga */
    .wheel-anim { animation: rotate 10s linear infinite; width: 120px; display: block; margin: auto; }
    @keyframes rotate { 100% { transform: rotate(360deg); } }
</style>
""", unsafe_allow_html=True)

# --- 3. RENDERIZADO DEL HEADER ---
st.markdown(f"""
