# app.py
import os
import streamlit as st

# --- Imports internos ---
from modulos.config.conexion import test_connection
from modulos.auth.auth import (
    create_user_table_if_not_exists,
    init_session,
    get_user_by_username,
    register_user,
    logout,
)
from werkzeug.security import check_password_hash
from modulos.ui_components.guide_page import render_guide_page

# Inicializar tabla auth y sesión
create_user_table_if_not_exists()
init_session()

# Ruta local al ER
logo_url = "file:///mnt/data/ER proyecto - ER NUEVO.pdf"

# Configuración de página
st.set_page_config(page_title="GAPC Portal", layout="wide", initial_sidebar_state="auto")

# ===============================
#      ESTILOS PREMIUM UI
# ===============================
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(135deg, #0f1724 0%, #071029 60%); color: #E6EEF8; }

    .login-wrap { display:flex; justify-content:center; padding:30px 12px; }
    .login-card { width:920px; border-radius:14px; padding:24px;
                  background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
                  border: 1px solid rgba(255,255,255,0.08);
                  box-shadow: 0 8px 30px rgba(2,6,23,0.6); }

    .login-grid { display: grid; grid-template-columns: 1fr 360px; gap: 22px; }

    .brand { display:flex; align-items:center; gap:14px; margin-bottom:10px; }
    .brand h1 { margin:0; font-size:42px; color:#F8FAFC; }
    .brand p { margin:0; color:#A5BBD8; font-size:14px; }

    .logo-box {
        width:74px; height:74px; border-radius:10px;
        background: linear-gradient(135deg, #1F3A93, #5C6BC0);
        display:flex; justify-content:center; align-items:center;
        color:white; font-weight:700; font-size:22px;
        box-shadow: 0 6px 18px rgba(10,20,40,0.5);
    }

    .login-title { color:#E6EEF8; font-size:24px; margin-bottom:8px; }
    .muted { color:#A7B8D8; font-size:13px; margin-bottom:12px; }

    .btn-small {
        background: transparent !important;
        color:#C7D9FF !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius:8px !important;
        padding:6px 10px !important;
        font-size:12px !important;
    }

    .tiny { color:#8EA7D1; font-size:12px; margin-top:8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ===============================
#         LOGIN PREMIUM
# ===============================
st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
st.markdown('<div class="login-card">', unsafe_allow_html=True)

# Branding superior
st.markdown(
    f'''
    <div class="brand">
      <div class="logo-box">G</div>
      <div>
        <h1>GAPC — Portal</h1>
        <p>Sistema de Gestión para Grupos de Ahorro y Préstamo Comunitarios</p>
      </div>
    </div>
    ''',
    unsafe_allow_html=True,
)

# GRID: Login grande + Registro compacto
st.markdown('<div class="login-grid">', unsafe_allow_html=True)

# -----------------------------------
#      COLUMNA IZQUIERDA: LOGIN
# -----------------------------------
st.markdown('<div>', unsafe_allow_html=True)
st.markdown('<div class="login-title">Iniciar sesión</div>', unsafe_allow_html=True)
st.markdown('<div class="muted">Introduce tus credenciales para acceder</div>', unsafe_allow_html=True)

with st.form(key="login_form_premium"):
    username = st.text_input("Usuario", placeholder="tu.usuario", label_visibility="collapsed")
    password = st.text_input("Contraseña", type="password", placeholder="••••••••", label_visibility="collapsed")

    cols = st.columns([1, 0.35])
    with cols[0]:
        submit_login = st.form_submit_button("Entrar")
    with cols[1]:
        st.markdown('<button class="btn-small" type="button">¿Olvidaste?</button>', unsafe_allow_html=True)

    if submit_login:
        if not username or not password:
            st.error("Completa usuario y contraseña.")
        else:
            u = get_user_by_username(username)
            if not u:
                st.error("Usuario no existe.")
            elif check_password_hash(u["password_hash"], password):
                st.session_state.user = {
                    "id": u["id"],
                    "username": u["username"],
                    "name": u.get("full_name"),
                    "role": u.get("role"),
                }
                st.success(f"Bienvenido {u.get('full_name') or u['username']}!")
                st.experimental_rerun()
            else:
                st.error("Contraseña incorrecta.")

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------
#      COLUMNA DERECHA: REGISTRO
# -----------------------------------
st.markdown('<div>', unsafe_allow_html=True)
st.markdown('<div class="login-title">Registrar usuario</div>', unsafe_allow_html=True)
st.markdown('<div class="muted">Acceso restringido</div>', unsafe_allow_html=True)

with st.form(key="register_small"):
    r_user = st.text_input("Usuario (nuevo)", placeholder="nuevo.usuario", label_visibility="collapsed")
    r_name = st.text_input("Nombre completo", placeholder="Nombre Apellido", label_visibility="collapsed")
    r_pw = st.text_input("Contraseña", type="password", placeholder="Crear contraseña", label_visibility="collapsed")
    r_pw2 = st.text_input("Confirmar contraseña", type="password", placeholder="Repetir contraseña", label_visibility="collapsed")

    cols = st.columns([1, 0.5])
    with cols[0]:
        submit_register = st.form_submit_button("Registrar")
    with cols[1]:
        st.markdown('<button class="btn-small" type="button">Ayuda</button>', unsafe_allow_html=True)

    if submit_register:
        if not r_user or not r_pw:
            st.error("Usuario y contraseña obligatorios.")
        elif r_pw != r_pw2:
            st.error("Las contraseñas no coinciden.")
        elif get_user_by_username(r_user):
            st.error("Usuario ya existe.")
        else:
            register_user(r_user, r_pw, r_name)
            st.success("Usuario registrado. Inicia sesión.")

# Link pequeño al ER
st.markdown(
    f'<div class="tiny">¿Necesitas ayuda? Mira el ER: <a href="{logo_url}" target="_blank" style="color:#CFE3FF">Ver ER</a></div>',
    unsafe_allow_html=True,
)

st.markdown('</div>', unsafe_allow_html=True)  # cierre col derecha
st.markdown('</div>', unsafe_allow_html=True)  # cierre grid
st.markdown('</div>', unsafe_allow_html=True)  # cierre card
st.markdown('</div>', unsafe_allow_html=True)  # cierre wrap

# ===============================
#   POST LOGIN (sidebar + menú)
# ===============================
if st.session_state.get("user"):

    st.sidebar.write(f"Conectado como: **{st.session_state.user['username']}**")

    if st.sidebar.button("Cerrar sesión"):
        logout()
        st.experimental_rerun()

    # Estado de la BD
    ok, msg = test_connection()
    if ok:
        st.sidebar.success("DB: conectado")
    else:
        st.sidebar.error("DB: no conectado")

    # Menú
    menu = st.sidebar.radio("Navegación", ["Dashboard", "Guía visual", "Miembros", "Aportes", "Préstamos", "Reportes"])

    if menu == "Guía visual":
        render_guide_page()
    elif menu == "Dashboard":
        st.header("Dashboard")
        st.write("KPIs pendientes de configurar…")
    else:
        st.header(menu)
        st.write("Página aún en construcción.")

else:
    st.stop()

