import streamlit as st
import plotly.graph_objects as go
import requests
import time
from datetime import datetime

# --- 1. CONFIGURACIÓN DE NÚCLEO ---
SALDO_REAL = 144.95
FACTOR = 32
ASSET = "RENDER (IA)"

st.set_page_config(layout="wide", page_title="MAHORASHARK V50")

# --- 2. EL MARTILLO: CSS DE GRADO MILITAR (CERO ESTILO WEB) ---
st.markdown(f"""
<style>
    /* Reset de UI y Fondo Dark Mode Profundo #0A0E14 */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {{display: none !important;}}
    .stApp {{ background-color: #0A0E14 !important; color: #00F2FF !important; }}
    
    /* Paneles con Profundidad y Capas (Glassmorphism) */
    .glass-card {{
        background: rgba(13, 17, 23, 0.85);
        border: 1px solid rgba(0, 242, 255, 0.1);
        padding: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.9), inset 0 0 20px rgba(0, 242, 255, 0.02);
        margin-bottom: 15px;
    }}

    /* Header Táctico Estrecho */
    .shark-hud {{
        display: flex; justify-content: space-between; align-items: center;
        background: #000; padding: 12px 30px;
        border-bottom: 2px solid #00F2FF;
        box-shadow: 0 5px 25px rgba(0, 242, 255, 0.2);
    }}
    .balance-glow {{
        font-family: 'Courier New', monospace;
        font-size: 42px; color: #39FF14; font-weight: bold;
        text-shadow: 0 0 20px rgba(57, 255, 20, 0.7);
    }}

    /* Botones de Activo (Sin estilo Streamlit) */
    .asset-row {{
        padding: 12px; border-bottom: 1px solid #1A1F26;
        font-family: 'Courier New', monospace; font-size: 11px;
        display: flex; justify-content: space-between; transition: 0.3s;
    }}
    .asset-row:hover {{ background: rgba(0, 242, 255, 0.1); border-left: 4px solid #00F2FF; }}
    .active-row {{ background: rgba(0, 242, 255, 0.15); border-left: 4px solid #00F2
