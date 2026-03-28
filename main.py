import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime
import time

# --- 1. NÚCLEO DE DATOS ---
SALDO_REAL = 144.95
STOCKS = [
    {"n": "RENDER (IA)", "p": 124.50, "c": "+2.4%"},
    {"n": "APPLE", "p": 3450.00, "c": "-0.1%"},
    {"n": "SAND", "p": 8.92, "c": "-1.5%"},
    {"n": "GALA", "p": 0.85, "c": "+5.2%"},
    {"n": "BITCOIN", "p": 1800000.0, "c": "+0.8%"}
]

st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA")

# --- 2. EL MARTILLO: INYECCIÓN DE ADN TÁCTICO (CSS) ---
st.markdown("""
<style>
    /* ELIMINAR CUALQUIER RASTRO DE STREAMLIT */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none !important;}
    .main { background-color: #000000 !important; }
    .block-container { padding: 5px !important; max-width: 98% !important; }
    
    /* FUENTE DE TERMINAL PURA */
    * { 
        color: #39FF14 !important; 
        font-family: 'Consolas', 'Lucida Console', monospace !important; 
        border-radius: 0px !important; 
    }
    
    /* HEADER CENTRALIZADO */
    .terminal-header { text-align: center; border-bottom: 1px solid #111; padding: 15px 0; margin-bottom: 20px; }
    .balance-neon { font-size: 58px; font-weight: 900; letter-spacing: -2px; text-shadow: 0 0 15px #39FF14; }
    .version-tag { font-size: 10px; color: #333 !important; letter-spacing: 5px; }

    /* PANELES LATERALES COMPACTOS */
    .panel-label { font-size: 11px; color: #444 !important; text-transform: uppercase; margin-bottom: 10px; border-bottom: 1px solid #111; }
    .asset-line
