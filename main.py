import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="Angel Prestige Center", page_icon="⛩️")

# --- 2. ESTILO CSS PROFESIONAL (FONDO Y CRISTAL) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)), 
                    url("https://get.wallhere.com/photo/digital-art-abstract-minimalism-geometry-dark-background-1563815.jpg");
        background-size: cover;
        color: white;
    }
    .main-title { text-align: center; color: #00f2ff; font-size: 32px; font-weight: bold; text-shadow: 0 0 20px #00f2ff; padding: 15px; }
    .kpi-card { 
        background: rgba(255, 255, 255, 0.05); 
        backdrop-filter: blur(10px); 
        border: 1px solid rgba(0, 242, 255, 0.3); 
        border-radius: 15px; padding: 15px; text-align: center;
    }
    .console-box { 
        background: rgba(0, 0, 0, 0.8); 
        border: 2px solid #ff00ff; 
        border-radius: 15px; padding: 20px; 
        font-family: 'Courier New', monospace; color: #39FF14; height: 550px;
    }
    .signal-buy { color: #39FF14; font-weight: bold; border: 2px solid #39FF14; padding: 10px; border-radius: 10px; text-align: center; background: rgba(57, 255, 20, 0.1); }
    .signal-sell { color: #ff00ff; font-weight: bold; border: 2px solid #ff00ff; padding: 10px; border-radius: 10px; text-align: center; background: rgba(255, 0, 255, 0.1); }
