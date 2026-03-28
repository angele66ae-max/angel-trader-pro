import streamlit as st
import plotly.graph_objects as go
import requests
import time
from datetime import datetime

# --- 1. SETTINGS DE ALTA PRIORIDAD ---
SALDO_REAL = 144.95
FACTOR = 32
ASSET = "RENDER (IA)"

st.set_page_config(layout="wide", page_title="MAHORASHARK V51", page_icon="🦈")

# --- 2. EL MARTILLO: CSS DE GRADO MILITAR (SIN FUGAS) ---
st.markdown(f"""
<style>
    /* Reset de UI y Fondo Dark #0A0E14 */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {{display: none !important;}}
    .stApp {{ background-color: #0A0E14 !important; color: #00F2FF !important; }}
    
    /* Paneles Glassmorphism */
    .glass-card {{
        background: rgba(13, 17, 23, 0.9);
        border: 1px solid rgba(0, 242, 255, 0.15);
        padding: 20px;
        border-radius: 2px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.9);
        margin-bottom: 15px;
    }}

    /* Header Táctico */
    .shark-hud {{
        display: flex; justify-content: space-between; align-items: center;
        background: #000; padding: 12px 30px;
        border-bottom: 2px solid #00F2FF;
        box-shadow: 0 5px 25px rgba(0, 242, 255, 0.2);
    }}
    .balance-glow {{
        font-family: 'Courier New', monospace;
        font-size: 40px; color: #39FF14; font-weight: bold;
        text-shadow: 0 0 15px rgba(57, 255, 20, 0.6);
    }}

    /* Listado de Activos */
    .asset-row {{
        padding: 12px; border-
