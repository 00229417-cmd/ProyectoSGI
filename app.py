# ================================
#   GAPC PORTAL — LOGIN ULTRA PREMIUM
# ================================

import streamlit as st
from werkzeug.security import check_password_hash

# --- Módulos internos ---
from modulos.config.conexion import test_connection
from modulos.auth.auth import (
    create_user_table_if_not_exists,
    init_session,
    get_user_by_username,
    register_user,
    logout,
)
from modulos.ui_components.guide_page import render_guide_page

# Inicialización
create_user_table_if_not_exists()
init_session()

# Ruta a tu ER como ayuda visual
logo_url = "file:///mnt/data/ER proyecto - ER NUEVO.pdf"

# Configuración de página
st.set_page_config(
    page_title="GAPC Portal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================================
# OCULTAR HEADER DE STREAMLIT
# ================================

hide_streamlit = """
<style>
header {visibility: hidden;}
main {padding-top: 0rem;}
</style>
"""
st.markdown(hide_streamlit, unsafe_allow_html=True)

# ================================
# ESTILOS ULTRA PREMIUM (CSS)
# ================================

st.markdown(
    """
<style>

.stApp {
  background: radial-gradient(circle at 8% 12%, rgba(50,80,150,0.22), transparent 40%),
              radial-gradient(circle at 92% 88%, rgba(10,40,80,0.20), transparent 40%),
              linear-gradient(180deg, #071528 0%, #030915 100%);
  font-family: 'Inter', sans-serif;
  color: #E9F0FF;
}

.ultra-wrap {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 30px 18px 80px 18px;
  margin-top: 5px;
}

.ultra-card {
  width: 960px;
  max-width: 96%;
  border-radius: 18px;
  padding: 26px;
  background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.06);
  box-shadow: 0 18px 50px rgba(0,0,0,0.45);
  backdrop-filter: blur(10px) saturate(130%);
  display:grid;
  grid-template-columns: 1fr 380px;
  gap: 26px;
  margin-top: -35px;
  animation: fadeIn 0.7s ease-out forwards;
}

@keyframes fadeIn {
  0% {opacity:0; transform: translateY(15px);}
  100% {opacity:1; transform: translateY(0);}
}

.ultra-card:hover {
  transform: translateY(-2px);
  transition: 0.3s ease-out;
}

.ultra-logo {
  width:80px; height:80px;
  border-radius:16px;
  background: linear-gradient(135deg,#6a9cff,#3f6bd6);
  display:flex; align-items:center; justify-content:center;
  font-size:34px; font-weight:800; color:white;
  box-shadow: 0 12px 28px rgba(50,100,255,0.35);
  animation: float 4s ease-in-out infinite;
}

@keyframes float {
  0% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
  100% { transform: translateY(0); }
}

.brand-title { 
  font-size:34px; 
  margin:0; 
  color:#F7FBFF;
}

.brand-sub { 
  color:#AABDDE; 
  font-size:13px;
}

.login-title {
  font-size:20px; 
  color:#EAF2FF; 
  margin-top:8px;
}

.login-desc {
  color:#A7B9DA;
  font-size:13px;
  margin-bottom:14px;
}

.side-card {
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  padding:18px;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,0.05);
}

.side-title { font-size:16px; color:#EAF2FF; }
.side-text { color:#9FB4D6; font-size:13px; }

.btn-ghost {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.12);
  color:#DDE9FF; padding:8px 12px;
  border-radius:10px; cursor:pointer;
}

.tiny { color:#8EA7D1; font-size:12px; margin-top:10px; display:block; }

@media (max-width: 900px) {
  .ultra-card { grid-template-columns: 1fr; }
  .ultra-logo { width:60px; height:60px; font-size:22px; }
}
</style>
""",
    unsafe_allow_html=True
)

# ===========================
# TARJETA ULTRA PREMIUM
# ===========================

st.markdown('<div class="ultra-wrap">', unsafe_allow_html=True)
st.markdown('<div class="ultra-card">', unsafe_allow_html=True)

# ---------------------
# COLUMNA IZQUIERDA
# ---------------------
st.markdown(
    """
    <div>
        <div style="display:flex; gap:14px; align-items:center;">
            <div class="ultra-logo">G</div>
            <div>
                <div class="brand-title">GAPC — Portal</div>
                <div class="brand-sub">Sistema de Gestión para Grupos de Ahorro y Préstamo Comunitarios</div>
            </div>
        </div>

        <div class="login-title">Iniciar sesión</div>
        <div class="login-desc">Accede con tu usuario y contraseña.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("ultra_login_form"):
    username = st.text_input("", placeholder="usuario.ejemplo", label_visibility="collapsed")
    password = st.text_input("", placeholder="Contraseña", type="password", label_visibility="collapsed")

    c1, c2 = st.columns([1,0.4])
    with c1:
        submit = st.form_submit_button("Entrar")
    with c2:
        st.markdown('<button class="btn-ghost" type="button">¿Olvidaste?</button>', unsafe_allow_html=True)

    if submit:
        if not username or not password:
            st.error("Completa usuario y contraseña.")
        else:
            u = get_user_by_username(username)
            if not u:
                st.error("Usuario no encontrado.")
            else:
                if check_password_hash(u["password_hash"], password):
                    st.success("¡Inicio de sesión exitoso!")
                    st.session_state.user = {
                        "id": u["id"],
                        "username": u["username"],
                        "name": u.get("full_name"),
                        "role": u.get("role"),
                    }
                    st.experimental_rerun()
                else:
                    st.error("Contraseña incorrecta.")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------
# COLUMNA DERECHA (registro)
# ---------------------
st.markdown('<div class="side-card">', unsafe_allow_html=True)

st.markdown(
    """
    <div class="side-title">Registrar usuario</div>
    <div class="side-text">Acceso limitado. Solo para nuevos administradores.</div>
    """,
    unsafe_allow_html=True
)

with st.form("ultra_register_form"):
    r_user = st.text_input("", placeholder="Nuevo usuario", label_visibility="collapsed")
    r_name = st.text_input("", placeholder="Nombre completo", label_visibility="collapsed")
    r_pw = st.text_input("", placeholder="Crear contraseña", type="password", label_visibility="collapsed")
    r_pw2 = st.text_input("", placeholder="Confirmar contraseña", type="password", label_visibility="collapsed")

    r1, r2 = st.columns([1,0.4])
    with r1:
        register_btn = st.form_submit_button("Registrar")
    with r2:
        st.markdown('<button class="btn-ghost">Ayuda</button>', unsafe_allow_html=True)

    if register_btn:
        if not r_user or not r_pw:
            st.error("Usuario y contraseña son obligatorios.")
        elif r_pw != r_pw2:
            st.error("Las contraseñas no coinciden.")
        elif get_user_by_username(r_user):
            st.error("Usuario ya existe.")
        else:
            register_user(r_user, r_pw, r_name)
            st.success("Usuario registrado correctamente.")

st.markdown(f'<a class="tiny" href="{logo_url}" target="_blank">Ver ER / Ayuda</a>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)   # ultra-card
st.markdown("</div>", unsafe_allow_html=True)   # ultra-wrap


# ===========================
#   POST LOGIN (sidebar)
# ===========================
if st.session_state.get("user"):

    # Sidebar
    st.sidebar.write(f"Conectado como **{st.session_state.user['username']}**")

    if st.sidebar.button("Cerrar sesión"):
        logout()
        st.experimental_rerun()

    ok, msg = test_connection()
    if ok:
        st.sidebar.success("DB: conectado")
    else:
        st.sidebar.error("DB: no conectado")

    menu = st.sidebar.radio(
        "Menú",
        ["Dashboard", "Guía visual", "Miembros", "Aportes", "Préstamos", "Reportes"]
    )

    if menu == "Guía visual":
        render_guide_page()
    else:
        st.header(menu)
        st.write("Página en construcción.")

else:
    st.stop()



