import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# --- DATOS DE ACCESO ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="MahoraShark Pro", page_icon="⛩️")

# --- DISEÑO CON FONDO CYBERPUNK Y GLOW ---
# Usamos el fondo de ciudad neón que definimos
fondo_url = "https://images.wallpapersden.com/image/download/cyberpunk-city-street-night-art_bgmqaGWUmZqaraWkpJRmbmdlrWZnZ2U.jpg"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url("{fondo_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    .metric-card {{
        background-color: rgba(11, 20, 26, 0.9);
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 20px #00f2ff66;
    }}
    .ia-log {{
        background-color: rgba(0, 0, 0, 0.9);
        border: 2px
