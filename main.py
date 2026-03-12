import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CREDENCIALES ---
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "").strip()

st.set_page_config(layout="wide", page_title="TERMINAL SHARK v6")

# --- ESTILO "MOVIE HACKER" ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp { 
        background-color: #05070a; 
        background-image: radial-gradient(#0a192f 0.5px, transparent 0.5px);
        background-size: 20px 20px;
        font-family: 'JetBrains Mono', monospace; 
    }
    
    /* Efecto Neón para métricas */
    div[data-testid="stMetricValue"] { 
        color: #00ff41 !important; 
        text-shadow: 0 0 10px #00ff41;
        font-size: 1.8rem !important;
    }
    
    /* Títulos tipo Terminal */
    h1, h2, h3 { 
        color: #00d4ff !important; 
        text-transform: uppercase;
        letter-spacing: 2px;
        border-left: 5px solid #00d4ff;
        padding-left: 15px;
    }

    /* Tablas estilo Cyberpunk */
    .stTable { 
        background: rgba(16, 20, 30, 0.9);
        border: 1px solid #00d4ff;
        border-radius: 10px;
    }
    
    .status-error {
        background: rgba(255, 0, 60, 0.1);
        border: 1px solid #ff003c;
        padding: 10px;
        color: #ff003c;
        animation: blinker 2s linear infinite;
    }

    @keyframes blinker { 50% { opacity: 0.5; } }
    </style>
    """, unsafe_allow_html=True)

class CyberEngine:
    def __init__(self, key, secret):
        self.key, self.secret = key, secret
        self.url = "https://api.bitso.com"

    def get_price(self, book):
        try:
            r = requests.get(f"{self.url}/v3/ticker/?book={book}").json()
