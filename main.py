import streamlit as st
import plotly.graph_objects as go
import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- 1. CONFIGURACIÓN DEL SISTEMA (SHARK CORE) ---
SALDO_REAL = 144.95
FACTOR = 32
ASSET = "RENDER (IA)"

st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA V61", page_icon="🦈")

# --- 2. EL MARTILLO: INYECCIÓN DE CSS CYBER-NOIR (MILITARY SPEC) ---
# Separado para evitar errores de sintaxis y asegurar el acabado profesional.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;900&display=swap');

    /* Reset total y fondo Deep Black #0A0E14 */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
    .stApp { background-color: #0A0E14 !important; color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    
    /* PANELES GLASSMORPHISM CON PROFUNDIDAD (Borde 1px) */
    .module-card {
        background: rgba(13, 17, 23, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 242, 255, 0.15);
        border-radius: 2px;
        padding: 15px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.9);
        margin-bottom: 12px;
    }

    /* HEADER TÁCTICO CON RESPLANDOR NEÓN */
    .nav-hud {
        display: flex; justify-content: space-between; align-items: center;
        background: #000; padding: 10px 35px;
        border-bottom: 1px solid #00F2FF;
        box-shadow: 0 5px 25px rgba(0, 242, 255, 0.15);
        position: sticky; top: 0; z-index: 99;
    }
    .main-balance {
        font-family: 'JetBrains Mono', monospace;
        font-size: 40px; color: #39FF14; font-weight: 800;
        text-shadow: 0 0 15px #39FF14, 0 0 30px rgba(57, 255, 20, 0.3);
    }

    /* TERMINAL DE LOGS (EFECTO FÓSFORO CRT) */
    .terminal-out {
        background: #000; padding: 12px; border-left: 3px solid #00F2FF;
        font-family: 'JetBrains Mono', monospace; font-size: 10px;
        color: #00F2FF; height: 160px; overflow: hidden;
        text-shadow: 0 0 5px rgba(0, 242, 255, 0.5);
    }
    .log-tag { color: #39FF14; text-shadow: 0 0 8px #39FF14; font-weight: bold; }

    /* RUEDA DE ADAPTACIÓN SVG (ANIMACIÓN MAHORAGA) */
    .wheel-container { text-align: center; padding: 20px 0; }
    .mahoraga-gear {
        width: 150px; animation: rotation 20s linear infinite;
        filter: drop-shadow(0 0 12px rgba(138, 43, 226, 0.6));
    }
    @keyframes rotation { 100% { transform: rotate(360deg); } }

    /* custom Scrollbar */
    ::-webkit-scrollbar { width: 3px; }
    ::-webkit-scrollbar-thumb { background: #00F2FF; }

    /* Botonera de Activos */
    .asset-row {
        display: flex; justify-content: space-between; padding: 10px;
        border-bottom: 1px solid #1A1F26; font-size: 11px; font-family: 'JetBrains Mono', monospace;
        transition: 0.2s; cursor: pointer;
    }
    .asset-row:hover { background: rgba(0, 242, 255, 0.05); }
    .active-asset { background: rgba(0, 242, 255,
