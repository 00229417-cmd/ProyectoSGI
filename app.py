# app.py 
import streamlit as st
from werkzeug.security import check_password_hash

# módulos internos
from modulos.config.conexion import test_connection
from modulos.auth.auth import (
    create_user_table_if_not_exists,
    init_session,
    get_user_by_username,
    register_user,
    logout,
)
from modulos.ui_components.guide_page import render_guide_page
from modulos.ui_components.cards import info_card, status_badge

# inicialización
create_user_table_if_not_exists()
init_session()

# ruta local a tu ER (archivo subido)
logo_url = "file:///mnt/data/ER proyecto - ER NUEVO.pdf"

# page config
st.set_page_config(page_title="GAPC Portal", layout="wide", initial_sidebar_state="collapsed")

# =========================
# CSS (solo CSS aquí)
# =========================
st.markdown(
    """
    <style>
    /* ocultar header streamlit por completo */
    header { visibility: hidden; }
    /* body */
    .stApp {
      background: linear-gradient(180deg,#061025 0%, #021022 100%);
      color: #EAF2FF;
      font-family: Inter, "Segoe UI", Roboto, Arial, sans-serif;
    }

    /* contenedor del card principal (arriba, no centrado vertical) */
    .wrap {
      display:flex;
      justify-content:center;
      padding: 28px 12px 60px 12px;
      margin-top: 6px;
    }

    .card {
      width: 980px;
      max-width: 96%;
      border-radius: 16px;
      padding: 22px;
      background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
      border: 1px solid rgba(255,255,255,0.04);
      box-shadow: 0 18px 50px rgba(0,0,0,0.5);
      display: grid;
      grid-template-columns: 1fr 380px;
      gap: 22px;
      margin-top: -26px; /* lo sube un poco */
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

# =========================
# Contenedor principal (uso de st containers y columnas para evitar HTML crudo)
# =========================
with st.container():
    st.markdown('<div class="wrap">', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # --- LEFT: Brand + Login (usar streamlit nativo para inputs) ---
    # Creamos una columna virtual dejando HTML para la estructura visual,
    # pero evitamos imprimir tags crudos en el contenido principal.
    left_col, right_col = st.columns([2.2, 1])

    with left_col:
        # header branding
        c1, c2 = st.columns([0.18, 1])
        with c1:
            st.markdown('<div class="logo-box">G</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="brand-title">GAPC — Portal</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="brand-sub">Sistema de Gestión para Grupos de Ahorro y Préstamo Comunitarios</div>', unsafe_allow_html=True)

        # Login title & description
        st.markdown('<div class="login-title">Iniciar sesión</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted">Accede con tu usuario y contraseña.</div>', unsafe_allow_html=True)

        # Formulario de login (usar st.form para control)
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
                                "role": u.get("role")
                            }
                            st.success(f"Bienvenido {u.get('full_name') or u['username']}!")
                            st.experimental_rerun()
                        else:
                            st.error("Contraseña incorrecta.")

    # --- RIGHT: Registro pequeño, ayuda y enlaces ---
    with right_col:
        st.markdown('<div class="side-card">', unsafe_allow_html=True)
        st.markdown('<div class="side-title"><b>Registrar usuario</b></div>', unsafe_allow_html=True)
        st.markdown('<div class="side-text">Acceso limitado. Solo para admins.</div>', unsafe_allow_html=True)

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
                    st.error("Usuario y contraseña obligatorios.")
                elif rp != rp2:
                    st.error("Las contraseñas no coinciden.")
                elif get_user_by_username(ru):
                    st.error("Usuario ya existe.")
                else:
                    register_user(ru, rp, rn)
                    st.success("Usuario registrado correctamente. Inicia sesión.")

        st.markdown(f'<a class="tiny" href="{logo_url}" target="_blank">Ver ER / Documentación</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)  # close side-card

    st.markdown('</div>', unsafe_allow_html=True)  # close card
    st.markdown('</div>', unsafe_allow_html=True)  # close wrap

# =======================================================
# POST-LOGIN: sidebar, estado DB y Dashboard Premium básico
# =======================================================
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
        # Dashboard premium: tarjetas KPI y gráficas (esqueleto)
        st.header("Dashboard — Resumen operativo")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total miembros", value= "—", delta="—")
            info_card("Ahorros totales", "Saldo consolidado por grupo", action_label="Ver Ahorros")
        with c2:
            st.metric("Préstamos vigentes", value="—", delta="—")
            info_card("Mora (%)", "Porcentaje de morosidad", action_label="Ver Morosidad")
        with c3:
            st.metric("Saldo caja", value="—", delta="—")
            info_card("Próximos cierres", "Ciclos próximos a cerrar", action_label="Ver cierres")

        st.markdown("---")
        st.subheader("Actividad reciente")
        st.write("Aquí irán las tablas y gráficas: movimientos, pagos recientes, solicitudes pendientes.")
        # ejemplo: tabla falsa
        st.table([{"evento":"Pago","miembro":"Juan","monto":"$20"},{"evento":"Aporte","miembro":"Ana","monto":"$5"}])

    else:
        st.header(menu)
        st.write("Página en construcción.")

else:
    st.stop()



