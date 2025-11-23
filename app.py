# ---------------------------
# ULTRA PREMIUM LOGIN (reemplazar la sección de login)
# ---------------------------
import streamlit as st
from modulos.auth.auth import (
    create_user_table_if_not_exists,
    init_session,
    get_user_by_username,
    register_user,
    logout,
)
from modulos.ui_components.guide_page import render_guide_page
from modulos.config.conexion import test_connection
from werkzeug.security import check_password_hash

# inicializa auth/session
create_user_table_if_not_exists()
init_session()

# Ruta a tu ER (puedes cambiar por /mnt/data/tu_logo.png si tienes imagen)
logo_url = "file:///mnt/data/ER proyecto - ER NUEVO.pdf"

st.set_page_config(page_title="GAPC Portal", layout="wide", initial_sidebar_state="auto")

# ---------------------------
# Ocultar header de Streamlit (si no lo quieres visible)
# ---------------------------
hide_streamlit_style = """
    <style>
    header {visibility: hidden;}
    main {padding-top: 0rem;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ---------------------------
# ULTRA PREMIUM STYLES + ANIM
# ---------------------------
st.markdown(
    """
    <style>
    /* Page gradient + subtle grain */
    .stApp {
      background: radial-gradient(circle at 10% 10%, rgba(31,58,93,0.85), transparent 20%),
                  radial-gradient(circle at 90% 90%, rgba(18,34,56,0.75), transparent 20%),
                  linear-gradient(180deg,#081126 0%,#041226 100%);
      color: #EAF2FF;
      font-family: Inter, "Segoe UI", Roboto, Arial, sans-serif;
    }

    /* Centering container full height */
    .ultra-wrap {
      min-height: calc(100vh - 10px);
      display:flex;
      align-items:center;
      justify-content:center;
      padding:48px 18px;
    }

    /* Glass card */
    .ultra-card {
      width: 960px;
      max-width: 96%;
      border-radius: 18px;
      padding: 28px;
      background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));
      border: 1px solid rgba(255,255,255,0.05);
      box-shadow: 0 20px 60px rgba(2,8,23,0.65);
      backdrop-filter: blur(8px) saturate(120%);
      display:grid;
      grid-template-columns: 1fr 420px;
      gap: 28px;
      align-items:center;
      transform: translateY(0px);
      transition: transform 0.45s cubic-bezier(.2,.9,.3,1);
    }
    .ultra-card:hover { transform: translateY(-6px); }

    /* Brand */
    .ultra-brand { display:flex; gap:16px; align-items:center; margin-bottom:6px; }
    .ultra-logo {
      width:84px; height:84px; border-radius:16px;
      background: linear-gradient(135deg,#6a9cff,#3f6bd6);
      display:flex; align-items:center; justify-content:center;
      color:white; font-weight:800; font-size:34px;
      box-shadow: 0 12px 30px rgba(33,78,161,0.32);
      animation: float 4s ease-in-out infinite;
    }
    @keyframes float {
      0% { transform: translateY(0); }
      50% { transform: translateY(-6px); }
      100% { transform: translateY(0); }
    }
    .brand-title { font-size:34px; margin:0; color:#F7FBFF; letter-spacing:0.6px; }
    .brand-sub { margin:0; color:#9BB1D6; font-size:13px; }

    /* Left (big login) */
    .login-title { font-size:20px; color:#EAF2FF; margin: 6px 0 8px 0; }
    .login-desc { color:#9FB4D6; font-size:13px; margin-bottom:14px; }

    .input-style {
      background: rgba(20,30,45,0.55);
      border: 1px solid rgba(255,255,255,0.04);
      padding: 12px 14px;
      border-radius: 10px;
      color: #EAF2FF;
      width:100%;
      box-sizing:border-box;
      margin-bottom:12px;
    }

    /* Buttons */
    .btn-primary {
      background: linear-gradient(90deg,#2b7bff,#4c6bf7);
      color:white; padding:10px 16px; border-radius:12px;
      border:none; box-shadow: 0 12px 24px rgba(35,80,200,0.18);
      cursor:pointer; font-weight:600;
    }
    .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 18px 40px rgba(35,80,200,0.22); }

    .btn-ghost {
      background: transparent;
      border: 1px solid rgba(255,255,255,0.06);
      color:#DDE9FF; padding:8px 12px; border-radius:10px; cursor:pointer;
    }

    /* Right (card info) */
    .side-card {
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border-radius: 12px;
      padding:18px;
      border: 1px solid rgba(255,255,255,0.04);
    }
    .side-title { font-size:16px; color:#EAF2FF; margin-bottom:6px; }
    .side-text { color:#9FB4D6; font-size:13px; margin-bottom:14px; }

    /* tiny footer */
    .tiny { color:#8EA7D1; font-size:12px; margin-top:10px; display:block; }

    /* responsive */
    @media (max-width: 900px) {
      .ultra-card { grid-template-columns: 1fr; padding:18px; }
      .ultra-logo { width:64px; height:64px; font-size:26px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# RENDER ULTRA CARD
# ---------------------------
st.markdown('<div class="ultra-wrap">', unsafe_allow_html=True)
st.markdown('<div class="ultra-card">', unsafe_allow_html=True)

# Brand header (left column top)
st.markdown(
    f'''
    <div>
      <div class="ultra-brand">
        <div class="ultra-logo">G</div>
        <div>
          <div class="brand-title">GAPC — Portal</div>
          <div class="brand-sub">Sistema de Gestión para Grupos de Ahorro y Préstamo Comunitarios</div>
        </div>
      </div>
      <div style="margin-top:6px;">
        <div class="login-title">Iniciar sesión</div>
        <div class="login-desc">Accede con tu usuario y contraseña para gestionar el grupo.</div>
      </div>
    ''',
    unsafe_allow_html=True,
)

# LEFT: Formulario (usamos streamlit para inputs pero con estilo visual)
with st.form(key="ultra_login_form"):
    col_username = st.text_input("", placeholder="usuario.ejemplo", key="ultra_user", label_visibility="collapsed")
    col_password = st.text_input("", placeholder="Contraseña", type="password", key="ultra_pw", label_visibility="collapsed")
    # Buttons row
    cl1, cl2 = st.columns([1, 0.35])
    with cl1:
        submitted = st.form_submit_button("Entrar")
    with cl2:
        st.markdown('<button class="btn-ghost" type="button">¿Olvidaste?</button>', unsafe_allow_html=True)

    if submitted:
        if not col_username or not col_password:
            st.error("Completa usuario y contraseña.")
        else:
            u = get_user_by_username(col_username)
            if not u:
                st.error("Usuario no encontrado.")
            else:
                if check_password_hash(u["password_hash"], col_password):
                    st.session_state.user = {
                        "id": u["id"],
                        "username": u["username"],
                        "name": u.get("full_name"),
                        "role": u.get("role"),
                    }
                    st.success(f"¡Bienvenido {u.get('full_name') or u['username']}!")
                    st.experimental_rerun()
                else:
                    st.error("Credenciales inválidas.")

# close left column div
st.markdown('</div>', unsafe_allow_html=True)

# RIGHT: side info / quick actions
st.markdown('<div class="side-card">', unsafe_allow_html=True)
st.markdown('<div class="side-title">Accesos rápidos</div>', unsafe_allow_html=True)
st.markdown('<div class="side-text">Registrar nuevo usuario (acceso limitado), ver documentación y generar reportes.</div>', unsafe_allow_html=True)

with st.form(key="ultra_register"):
    r_u = st.text_input("", placeholder="Nuevo usuario", key="ultra_reg_user", label_visibility="collapsed")
    r_n = st.text_input("", placeholder="Nombre completo", key="ultra_reg_name", label_visibility="collapsed")
    r_p = st.text_input("", placeholder="Contraseña", type="password", key="ultra_reg_pw", label_visibility="collapsed")
    r_p2 = st.text_input("", placeholder="Confirmar contraseña", type="password", key="ultra_reg_pw2", label_visibility="collapsed")
    rr1, rr2 = st.columns([1, 0.5])
    with rr1:
        reg_btn = st.form_submit_button("Registrar")
    with rr2:
        st.markdown('<button class="btn-ghost" type="button">Ayuda</button>', unsafe_allow_html=True)

    if reg_btn:
        if not r_u or not r_p:
            st.error("Usuario y contraseña obligatorios.")
        elif r_p != r_p2:
            st.error("Las contraseñas no coinciden.")
        elif get_user_by_username(r_u):
            st.error("Usuario ya existe.")
        else:
            register_user(r_u, r_p, r_n)
            st.success("Usuario registrado. Inicia sesión.")

# tiny ER link + close side
st.markdown(f'<a class="tiny" href="{logo_url}" target="_blank" style="color:#CFE3FF">Ver ER y documentación</a>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)  # close side-card

# close ultra-card + wrap
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# POST-LOGIN: sidebar / estado BD
# ---------------------------
if st.session_state.get("user"):
    st.sidebar.write(f"Conectado: **{st.session_state.user['username']}**")
    if st.sidebar.button("Cerrar sesión"):
        logout()
        st.experimental_rerun()

    ok, msg = test_connection()
    if ok:
        st.sidebar.success("DB: conectado")
    else:
        st.sidebar.error("DB: no conectado")

    menu = st.sidebar.radio("Navegación", ["Dashboard", "Guía visual", "Miembros", "Aportes", "Préstamos", "Reportes"])
    if menu == "Guía visual":
        render_guide_page()
    else:
        st.header(menu)
        st.write("Página en construcción.")
else:
    st.stop()


