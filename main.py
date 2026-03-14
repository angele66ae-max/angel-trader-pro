import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- CONFIGURACIÓN DE NÚCLEO ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: REAL-TIME")

# --- MEMORIA DE SESIÓN (Evita que la IA "olvide" o se trabe) ---
if "precios" not in st.session_state:
    # Iniciamos con datos base cerca del precio real de tus capturas
    st.session_state.precios = list(np.random.normal(70965, 10, size=50))
if "logs" not in st.session_state:
    st.session_state.logs = [f"[{datetime.now().strftime('%H:%M:%S')}] PROTOCOLO ACTIVADO. BUSCANDO META 10K..."]

# --- VARIABLES DE TU BALANCE REAL ---
META = 10000.0
balance = 2.81
progreso_pct = (balance / META) * 100

# --- ESTILO PRESTIGE ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: white; }
    .card {
        background: rgba(10, 15, 20, 0.9);
        border: 1px solid #00f2ff;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#00f2ff;'>⛩️ MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)

# Dashboard Superior
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="card">MOTOR IA<br><h2 style="color:#00ff00;">ADAPTANDO</h2></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="card">BALANCE REAL<br><h2 style="color:magenta;">${balance:.
