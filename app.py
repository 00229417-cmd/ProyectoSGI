# modulos/login.py
import streamlit as st
from werkzeug.security import check_password_hash

from modulos.auth.auth import (
    create_user_table_if_not_exists,
    init_session,
    get_user_by_username,
    register_user,
)

# Asegura tabla y sesión
create_user_table_if_not_exists()
init_session()

def login_page(logo_path: str = None):
    """
    Página de login + registro interactivo (registro aparece con botón).
    - El panel derecho con "Documentación / Contacto" ha sido eliminado (no aparece).
    - El botón 'Registrar usuario' queda justo debajo del login y abre el formulario en un expander.
    """

    # CSS premium + animaciones sutiles (entrada + movimiento)
    st.markdown(
        """
        <style>
        header { visibility: hidden; }
        main { padding-top: 0rem; }

        .login-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
            border-radius:12px;
            padding:18px;
            box-shadow:0 12px 30px rgba(0,0,0,0.45);
            animation: fadeInUp 0.6s ease-out both;
        }

        /* entrada */
        @keyframes fadeInUp {
          0% { opacity: 0; transform: translateY(12px); }
          100% { opacity: 1; transform: translateY(0); }
        }

        /* logo con leve movimiento flotante */
        .logo-small {
          width:76px; height:76px; border-radius:14px;
          background: linear-gradient(135deg,#5b8bff,#3c67d6);
          display:flex; align-items:center; justify-content:center;
          color:white; font-weight:800; font-size:28px;
          box-shadow: 0 10px 36px rgba(20,40,120,0.28);
          animation: floaty 6s ease-in-out infinite;
        }

        @keyframes floaty {
          0% { transform: translateY(0px); }
          50% { transform: translateY(-6px); }
          100% { transform: translateY(0px); }
        }

        .brand-title { font-size:28px; margin:0; color:#F7FBFF; }
        .brand-sub { font-size:13px; color:#9FB4D6; margin-top:6px; }

        .login-title { font-size:18px; color:#EAF2FF; margin-top:6px; }
        .muted { color:#9FB4D6; font-size:13px; margin-bottom:8px; }

        .small-btn {
          display:inline-block;
          border-radius:8px;
          padding:8px 10px;
          border:1px solid rgba(255,255,255,0.06);
          background: rgba(255,255,255,0.01);
          color:#DDEEFF;
          font-size:13px;
          cursor:pointer;
        }

        .register-expander .streamlit-expanderHeader {
          border-radius:8px;
        }

        /* Formato del formulario */
        .st-form {
          margin-top: 6px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # layout: dos columnas (contenido principal + columna derecha vacía/limpia)
    col_main, col_right = st.columns([1.8, 0.9])

    with col_main:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        # Branding
        col_logo, col_brand = st.columns([0.14, 1])
        with col_logo:
            st.markdown('<div class="logo-small">G</div>', unsafe_allow_html=True)
        with col_brand:
            st.markdown('<div class="brand-title">GAPC — Portal</div>', unsafe_allow_html=True)
            st.markdown('<div class="brand-sub">Sistema de Gestión para Grupos de Ahorro y Préstamo Comunitarios</div>', unsafe_allow_html=True)

        # Título y descripción
        st.markdown('<div class="login-title">Iniciar sesión</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted">Accede con tu usuario y contraseña.</div>', unsafe_allow_html=True)

        # FORMULARIO DE LOGIN (st.form)
        with st.form(key="form_login", clear_on_submit=False):
            username = st.text_input("Usuario", placeholder="usuario.ejemplo", label_visibility="collapsed")
            password = st.text_input("Contraseña", type="password", placeholder="Contraseña", label_visibility="collapsed")
            # Botones: Entrar + pequeño Registrar usuario (debajo)
            col_a, col_b = st.columns([0.6, 0.4])
            with col_a:
                btn_login = st.form_submit_button("Entrar")
            with col_b:
                # botón pequeño que activa mostrar el registro
                if st.form_submit_button("Registrar usuario", use_container_width=True, key="open_register_btn"):
                    # usare session_state para mostrar el expander de registro
                    st.session_state.setdefault("mostrar_registro", True)

            # proceso login
            if btn_login:
                if not username or not password:
                    st.error("Completa usuario y contraseña.")
                else:
                    u = get_user_by_username(username)
                    if not u:
                        st.error("Usuario no encontrado.")
                    else:
                        if check_password_hash(u["password_hash"], password):
                            st.session_state["session_iniciada"] = True
                            st.session_state["usuario"] = username
                            st.session_state["usuario_id"] = u.get("id")
                            st.success(f"Bienvenido {u.get('full_name') or username}!")
                            # rerun para recargar UI (login desaparece)
                            try:
                                st.rerun()
                            except Exception:
                                # fallback si versión antigua
                                st.experimental_rerun()
                        else:
                            st.error("Contraseña incorrecta.")

        # Espacio pequeño
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # EXPANDER / FORMULARIO DE REGISTRO (se muestra si session_state['mostrar_registro'] True)
        show_reg = st.session_state.get("mostrar_registro", False)
        exp = st.expander("Registrar usuario" if not show_reg else "Registrar usuario (ocultar)", expanded=show_reg)
        with exp:
            with st.form(key="form_register"):
                r_user = st.text_input("Usuario (nuevo)", placeholder="nuevo.usuario", label_visibility="collapsed")
                r_name = st.text_input("Nombre completo", placeholder="Nombre Apellido", label_visibility="collapsed")
                r_pwd = st.text_input("Contraseña", type="password", placeholder="Crear contraseña", label_visibility="collapsed")
                r_pwd2 = st.text_input("Confirmar contraseña", type="password", placeholder="Confirmar contraseña", label_visibility="collapsed")
                rcol1, rcol2 = st.columns([0.7, 0.3])
                with rcol1:
                    btn_reg = st.form_submit_button("Registrar")
                with rcol2:
                    if st.form_submit_button("Cancelar", key="cancel_reg"):
                        st.session_state["mostrar_registro"] = False
                if btn_reg:
                    if not r_user or not r_pwd:
                        st.error("Usuario y contraseña obligatorios.")
                    elif r_pwd != r_pwd2:
                        st.error("Las contraseñas no coinciden.")
                    elif get_user_by_username(r_user):
                        st.error("Usuario ya existe.")
                    else:
                        ok = register_user(r_user, r_pwd, full_name=r_name)
                        if ok:
                            st.success("Usuario registrado correctamente. Inicia sesión.")
                            # ocultar automáticamente el registro
                            st.session_state["mostrar_registro"] = False
                        else:
                            st.error("No se pudo registrar el usuario (revisar logs).")

        # cierre del card
        st.markdown('</div>', unsafe_allow_html=True)

    # columna derecha: la dejamos limpia (sin mostrar Documentación ni Contacto)
    with col_right:
        # espacio reservado para ayudas futuras, dejamos vacío intencionalmente
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        # si quieres mantener un pequeño "help" escondido, puedes activarlo más tarde.



