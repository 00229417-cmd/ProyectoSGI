# app.py 
import streamlit as st
from werkzeug.security import check_password_hash

# módulos internos (asegúrate de que existen en tu repo)
from modulos.config.conexion import test_connection
from modulos.auth.auth import (
    create_user_table_if_not_exists,
    init_session,
    get_user_by_username,
    register_user,
    logout,
)
from modulos.ui_components.guide_page import render_guide_page

# Inicializaciones
create_user_table_if_not_exists()
init_session()

# Ruta local a tu ER (archivo subido)
logo_url = "file:///mnt/data/ER proyecto - ER NUEVO.pdf"

# Configuración de la página
st.set_page_config(page_title="GAPC Portal", layout="wide", initial_sidebar_state="collapsed")

# ---------------------------
# Ocultar header (barra superior) y CSS global
# ---------------------------
st.markdown(
    """
    <style>
    /* ocultar header de Streamlit */
    header { visibility: hidden; }
    main { padding-top: 0rem; }

    /* fondo y tipografía */
    .stApp {
      background: linear-gradient(180deg,#071528 0%, #030915 100%);
      color: #EAF2FF;
      font-family: Inter, "Segoe UI", Roboto, Arial, sans-serif;
    }

    /* contenedor principal (arriba de la pantalla, no centrado vertical) */
    .wrap {
      display:flex;
      justify-content:center;
      padding: 26px 12px 60px 12px;
      margin-top: 6px;
    }

    /* tarjeta principal */
    .card {
      width: 980px;
      max-width: 96%;
      border-radius: 16px;
      padding: 22px;
      background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
      border: 1px solid rgba(255,255,255,0.04);
      box-shadow: 0 18px 50px rgba(0,0,0,0.45);
      display: grid;
      grid-template-columns: 1fr 380px;
      gap: 22px;
      margin-top: -26px;
      animation: fadeIn 0.6s ease-out forwards;
    }
    @keyframes fadeIn {
      0% { opacity: 0; transform: translateY(12px); }
      100% { opacity: 1; transform: translateY(0); }
    }

    .logo-box {
      width:72px; height:72px; border-radius:12px;
      background: linear-gradient(135deg,#5b8bff,#3c67d6);
      display:flex; align-items:center; justify-content:center;
      color:white; font-weight:700; font-size:26px;
      box-shadow: 0 10px 26px rgba(40,80,200,0.28);
    }

    .brand-title { font-size:32px; margin:0; color:#F7FBFF; }
    .brand-sub { font-size:13px; color:#9FB4D6; margin-top:4px; }

    .login-title { font-size:20px; color:#EAF2FF; margin-top:6px; }
    .muted { color:#9FB4D6; font-size:13px; margin-bottom:10px; }

    .side-card { padding:14px; border-radius:12px; background: rgba(255,255,255,0.01); border:1px solid rgba(255,255,255,0.03); }

    .btn-ghost {
      background: transparent; border:1px solid rgba(255,255,255,0.06);
      color:#DCEBFF; padding:8px 10px; border-radius:10px;
    }

    .tiny { color:#8EA7D1; font-size:12px; margin-top:8px; display:block; }

    @media (max-width: 880px) {
      .card { grid-template-columns: 1fr; margin-top: 0; }
      .logo-box { width:60px; height:60px; font-size:20px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Contenedor principal sin imprimir HTML como texto
# ---------------------------
with st.container():
    # estructura: wrapper + card (marca visual con CSS, no contenido HTML suelto)
    st.markdown('<div class="wrap">', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # Usamos columnas nativas de Streamlit para el layout interno
    left_col, right_col = st.columns([2.2, 1])

    # ------------- COLUMNA IZQUIERDA: BRAND + LOGIN -------------
    with left_col:
        # Branding (HTML pequeño controlado con markdown)
        cols_brand = st.columns([0.18, 1])
        with cols_brand[0]:
            st.markdown('<div class="logo-box">G</div>', unsafe_allow_html=True)
        with cols_brand[1]:
            st.markdown('<div class="brand-title">GAPC — Portal</div>', unsafe_allow_html=True)
            st.markdown('<div class="brand-sub">Sistema de Gestión para Grupos de Ahorro y Préstamo Comunitarios</div>', unsafe_allow_html=True)

        # Títulos (renderizados con markdown, no con st.write)
        st.markdown('<div class="login-title">Iniciar sesión</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted">Accede con tu usuario y contraseña.</div>', unsafe_allow_html=True)

        # Formulario de login (st.form para control)
        with st.form(key="login_form"):
            usuario = st.text_input("Usuario", placeholder="usuario.ejemplo", label_visibility="collapsed")
            clave = st.text_input("Contraseña", type="password", placeholder="Contraseña", label_visibility="collapsed")
            col_a, col_b = st.columns([1, 0.35])
            with col_a:
                entrar = st.form_submit_button("Entrar")
            with col_b:
                st.markdown('<button class="btn-ghost" type="button">¿Olvidaste?</button>', unsafe_allow_html=True)

            if entrar:
                if not usuario or not clave:
                    st.error("Completa usuario y contraseña.")
                else:
                    u = get_user_by_username(usuario)
                    if not u:
                        st.error("Usuario no encontrado.")
                    else:
                        if check_password_hash(u["password_hash"], clave):
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

    # ------------- COLUMNA DERECHA: REGISTRO + HELP -------------
    with right_col:
        st.markdown('<div class="side-card">', unsafe_allow_html=True)
        st.markdown('<div class="side-title"><b>Registrar usuario</b></div>', unsafe_allow_html=True)
        st.markdown('<div class="side-text">Acceso limitado. Solo para administradores.</div>', unsafe_allow_html=True)

        with st.form("register_form"):
            ru = st.text_input("Usuario (nuevo)", placeholder="nuevo.usuario", label_visibility="collapsed")
            rn = st.text_input("Nombre completo", placeholder="Nombre Apellido", label_visibility="collapsed")
            rp = st.text_input("Contraseña", type="password", placeholder="Crear contraseña", label_visibility="collapsed")
            rp2 = st.text_input("Confirmar contraseña", type="password", placeholder="Confirmar contraseña", label_visibility="collapsed")
            rcol1, rcol2 = st.columns([1, 0.4])
            with rcol1:
                reg_btn = st.form_submit_button("Registrar")
            with rcol2:
                st.markdown('<button class="btn-ghost">Ayuda</button>', unsafe_allow_html=True)

            if reg_btn:
                if not ru or not rp:
                    st.error("Usuario y contraseña son obligatorios.")
                elif rp != rp2:
                    st.error("Las contraseñas no coinciden.")
                elif get_user_by_username(ru):
                    st.error("Usuario ya existe.")
                else:
                    register_user(ru, rp, rn)
                    st.success("Usuario registrado correctamente. Inicia sesión.")

        # Enlace al ER (ayuda)
        st.markdown(f'<a class="tiny" href="{logo_url}" target="_blank">Ver ER / Documentación</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)  # close side-card

    st.markdown('</div>', unsafe_allow_html=True)  # close card
    st.markdown('</div>', unsafe_allow_html=True)  # close wrap

# ---------------------------
# POST-LOGIN: sidebar + dashboard básico
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

    elif menu == "Dashboard":
        st.header("Dashboard — Resumen")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total miembros", value="—")
            st.write("Ahorros totales: —")
        with c2:
            st.metric("Préstamos vigentes", value="—")
            st.write("Mora (%): —")
        with c3:
            st.metric("Saldo caja", value="—")
            st.write("Próximos cierres: —")

        st.markdown("---")
        st.subheader("Actividad reciente")
        st.table([{"evento": "Pago", "miembro": "Juan", "monto": "$20"}, {"evento": "Aporte", "miembro": "Ana", "monto": "$5"}])

    else:
        st.header(menu)
        st.write("Página en construcción.")
else:
    st.stop()




