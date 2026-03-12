import streamlit as st
import time, requests, hashlib, hmac, os
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- SHARK AUTH ---
API_KEY = st.secrets.get("BITSO_API_KEY", "").strip()
API_SECRET = st.secrets.get("BITSO_API_SECRET", "").strip()

st.set_page_config(layout="wide", page_title="SHARK TANK | PRO TRADER")

# --- TRADINGVIEW DARK STYLE ---
st.markdown("""
    <style>
    .stApp { background: #131722; color: #d1d4dc; font-family: 'Trebuchet MS', sans-serif; }
    .stMetric { background: #1e222d; border: 1px solid #363a45; border-radius: 5px; padding: 10px; }
    h1, h2, h3 { color: #2962ff !important; text-align: left; }
    .shark-log { 
        background: #1e222d; border: 1px solid #363a45; padding: 15px; 
        font-family: 'Consolas', monospace; color: #00ff88; height: 350px; overflow-y: scroll;
    }
    div[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 24px !important; }
    </style>
    """, unsafe_allow_html=True)

class SharkEngine:
    def __init__(self):
        self.base = "https://api.bitso.com"
        self.assets = ["btc_mxn", "eth_mxn", "usd_mxn", "nvda_usd", "aapl_usd", "msft_usd"]

    def get_balances(self):
        if not API_KEY: return None, "MISSING_KEYS"
        path = "/v3/balances/"
        nonce = str(int(time.time() * 1000))
        signature = hmac.new(API_SECRET.encode(), (nonce + "GET" + path).encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso
