# app.py
import os
import streamlit as st

# --- Conexión y utilidades ---
from modulos.config.conexion import test_connection
from modulos.auth.auth import (
    create_user_table_if_not_exists,
    init_session,
    get_user_by_username,
    register_user,
    logout,
)
# UI / ayuda
from modulos.ui_components.guide_page import render_guide_page

# seguridad (hash)
from werkzeug.security import check_password_hash

# Inicializaciones
create_user_table_if_not_exists()
init_session()

# Ruta local a tu ER (archivo subido). Se puede usar como enlace en la app.
logo_url = "file:///mnt/data/ER proyecto - ER NUEVO.pdf"

# Page config
st.set_page_config(page_title="GAPC Portal", layout="wide", initial_sidebar_state="auto")

# -----------------------
# DEBUG TEMPORAL (muestra URI parcial y test de conexión)
# - Mantener solo mientras depuramos la conexión.
# - Quitar después de que todo esté correcto.
# -----------------------
st.markdown("#### DEBUG (temporal) — información de conexión")
db_uri = os.getenv("MYSQL_ADDON_URI") or os.getenv("DATABASE_URL") or "NO_URI"
display = db_uri
if db_uri != "NO_URI":
    try:
        # ocultar la parte del usuario/contraseña para evitar exponer credenciales en logs
        if "@" in db_uri:
            parts = db_uri.split("@")
            host_part = parts[-1]
            display = "*****@{}".format(host_part)
    except Exception:
        display = "PARCIAL"
st.write("DB URI detectada (parcial):", display)

ok, msg = (False, "no probado")
try:
    ok, msg = test_connection()
except Exception as e:
    ok, msg = False, f"Error al probar conexión: {e}"

st.write("Test connection:", ok, "-", msg)
st.markdown("---")
# ----------------------- end DEBUG TEMPORAL -----------------------

# ---------------------------
# Custom CSS + PREMIUM login UI
# ---------------------------
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(135deg, #0f1724 0%, #071029 60%); color: #E6EEF8; }
    .login-wrap { display:flex; align-items:center; justify-content:center; padding:30px 12px; }
    .login-card { width:920px; border-radius:14px; padding:24px; box-shadow: 0 8px 30px rgba(2,6,23,0.6);
                  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
                  border: 1px solid rgba(255,255,255,0.04); }
    .login-grid { display: grid; grid-template-columns: 1fr 360px; gap: 22px; }
    .brand { display:flex; align-items:center; gap:14px; margin-bottom:6px; }
    .brand h1 { margin:0; font-size:40px; color:#F8FAFC; letter-spacing:1px; }
    .brand p { margin:0; color:#9FB4D6; font-size:13px; }
    .logo-box { width:74px; height:74px; border-radius:10px; background: linear-gradient(135deg, #1F3A93, #5C6BC0);
                display:flex; align-items:center; justify-content:center; color:white; font-weight:700; font-size:18px;
                box-shadow: 0 6px 18px rgba(10,20,40,0.5); }
    .login-title { font-size:22px; color:#E6EEF8; margin-bottom:8px; }
    .muted { color:#9FB4D6; font-size:13px; margin-bottom:14px; }
    .btn-primary { background:#1F6FEB !important; color:white !important; border-radius:8px !important;
                   padding:8px 16px !important; box-shadow: 0 6px 16px rgba(31,111,235,0.18) !important; border: none !important; }
    .btn-small { background: transparent !important; color:#BFD7FF !important;
                 border: 1px solid rgba(255,255,255,0.06) !important; border-radius:8px !important;
                 padding:6px 10px !important; font-size:13px !important; }
    .tiny { color:#8EA7D1; font-size:12px; margin-top:8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# RENDER LOGIN CARD
# ---------------------------
st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
st.markdown('<div class="login-card">', unsafe_allow_html=True)

# Header brand
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

st.markdown('<div class="login-grid">', unsafe_allow_html=True)

# LEFT: BIG LOGIN (custom form)
st.markdown('<div>', unsafe_allow_html=True)
st.markdown('<div class="login-title">Iniciar sesión</div>', unsafe_allow_html=True)
st.markdown('<div class="muted">Introduce tu usuario y contraseña para acceder al sistema</div>', unsafe_allow_html=True)

with st.form(key="premium_login_form"):
    username = st.text_input("Usuario", placeholder="tu.usuario", key="premium_user", label_visibility="collapsed")
    password = st.text_input("Contraseña", type="password", placeholder="••••••••", key="premium_pw", label_visibility="collapsed")
    cols = st.columns([1, 0.38])
    with cols[0]:
        submit = st.form_submit_button("Entrar", help="Acceder al sistema", key="premium_login_btn")
    with cols[1]:
        st.markdown('<div style="display:flex;align-items:center;height:100%;">', unsafe_allow_html=True)
        st.markdown('<button class="btn-small" type="button">¿Olvidaste?</button>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        # autenticación usando la tabla usuario_auth
        if not username or not password:
            st.error("Completa usuario y contraseña.")
        else:
            u = get_user_by_username(username)
            if not u:
                st.error("Usuario no encontrado.")
            else:
                # u['password_hash'] contiene hash
                if check_password_hash(u["password_hash"], password):
                    st.session_state.user = {
                        "id": u["id"],
                        "username": u["username"],
                        "name": u.get("full_name"),
                        "role": u.get("role"),
                    }
                    st.success(f"¡Bienvenido {u.get('full_name') or u['username']}!")
                    st.experimental_rerun()
                else:
                    st.error("Usuario o contraseña inválidos.")

st.markdown('</div>', unsafe_allow_html=True)  # end left column

# RIGHT: SMALL REGISTER + HELP
st.markdown('<div style="padding-left:6px;">', unsafe_allow_html=True)
st.markdown('<div class="login-title">Registrar nuevo usuario</div>', unsafe_allow_html=True)
st.markdown('<div class="muted">Registra un acceso (usuarios limitados).</div>', unsafe_allow_html=True)

with st.form(key="mini_register_form"):
    r_user = st.text_input("Usuario (nuevo)", placeholder="nuevo.usuario", key="mini_reg_user", label_visibility="collapsed")
    r_name = st.text_input("Nombre completo", placeholder="Nombre Apellido", key="mini_reg_name", label_visibility="collapsed")
    r_pw = st.text_input("Contraseña", type="password", placeholder="Crear contraseña", key="mini_reg_pw", label_visibility="collapsed")
    r_pw2 = st.text_input("Confirmar contraseña", type="password", placeholder="Repetir contraseña", key="mini_reg_pw2", label_visibility="collapsed")
    reg_cols = st.columns([1, 0.6])
    with reg_cols[0]:
        reg = st.form_submit_button("Registrar", key="mini_reg_btn")
    with reg_cols[1]:
        st.markdown('<div style="display:flex;justify-content:flex-end;"><button class="btn-small" type="button">Ayuda</button></div>', unsafe_allow_html=True)

    if reg:
        if not r_user or not r_pw:
            st.error("Usuario y contraseña obligatorios.")
        elif r_pw != r_pw2:
            st.error("Las contraseñas no coinciden.")
        elif get_user_by_username(r_user):
            st.error("Usuario ya existe.")
        else:
            register_user(r_user, r_pw, r_name)
            st.success("Usuario registrado con éxito. Inicia sesión.")

# link tiny + help (ER)
st.markdown(f'<div class="tiny">¿Necesitas ayuda? Consulta el ER: <a href="{logo_url}" target="_blank" style="color:#CFE3FF">ER de datos</a></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # end right
st.markdown('</div>', unsafe_allow_html=True)  # end grid
st.markdown('</div>', unsafe_allow_html=True)  # end card
st.markdown('</div>', unsafe_allow_html=True)  # end wrap

# ---------------------------
# AFTER LOGIN: show sidebar + navigation
# ---------------------------
if st.session_state.get("user"):
    st.sidebar.write(f"Conectado: {st.session_state.user['username']}")
    if st.sidebar.button("Cerrar sesión"):
        logout()
        st.experimental_rerun()

# quick connection status (repeat concise)
ok, msg = test_connection()
if ok:
    st.sidebar.success("DB: conectado")
else:
    st.sidebar.error("DB: no conectado")

# Navigation for logged users
if st.session_state.get("user"):
    menu = st.sidebar.radio("Navegación", ["Dashboard", "Guía visual", "Miembros", "Aportes", "Préstamos", "Reportes"])
    if menu == "Guía visual":
        render_guide_page()
    elif menu == "Dashboard":
        st.header("Dashboard (pendiente integrar)")
        st.write("Aquí irán KPIs y vistas principales.")
    else:
        st.header(menu)
        st.write("Página en construcción: pronto aquí podrá gestionar", menu)
else:
    # no user logged: stop further content (already shown login)
    st.stop()

