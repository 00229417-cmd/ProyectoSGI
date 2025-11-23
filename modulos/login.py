# modulos/login.py
import streamlit as st
from werkzeug.security import check_password_hash

from modulos.auth.auth import create_user_table_if_not_exists, init_session, get_user_by_username, register_user

# aseguramos tabla / session
create_user_table_if_not_exists()
init_session()

def login_page(logo_path: str = None):
    """
    Página de login + registro apilado.
    Al autenticar setea:
        st.session_state['session_iniciada'] = True
        st.session_state['usuario'] = username
        st.session_state['usuario_id'] = id
    """

    # CSS ligero (puedes ampliar)
    st.markdown(
        """
        <style>
        .login-card { background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
                      border-radius:12px; padding:18px; box-shadow:0 10px 30px rgba(0,0,0,0.5);}
        .logo-small { width:64px; height:64px; border-radius:10px; background:linear-gradient(135deg,#5b8bff,#3c67d6); display:flex; align-items:center; justify-content:center; font-weight:700; color:white;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 0.45])
    with col1:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        # branding
        brand_cols = st.columns([0.14, 1])
        with brand_cols[0]:
            st.markdown('<div class="logo-small">G</div>', unsafe_allow_html=True)
        with brand_cols[1]:
            st.title("GAPC — Portal")
            st.write("Sistema de Gestión para Grupos de Ahorro y Préstamo Comunitarios")

        st.subheader("Iniciar sesión")
        with st.form("form_login"):
            username = st.text_input("Usuario", placeholder="usuario.ejemplo", label_visibility="collapsed")
            password = st.text_input("Contraseña", type="password", placeholder="Contraseña", label_visibility="collapsed")
            submitted = st.form_submit_button("Entrar")
            if submitted:
                if not username or not password:
                    st.error("Ingresa usuario y contraseña.")
                else:
                    u = get_user_by_username(username)
                    if not u:
                        st.error("Usuario no encontrado.")
                    else:
                        if check_password_hash(u["password_hash"], password):
                            # set session
                            st.session_state["session_iniciada"] = True
                            st.session_state["usuario"] = username
                            st.session_state["usuario_id"] = u["id"]
                            st.success(f"Bienvenido {u.get('full_name') or username}!")
                            st.experimental_rerun()  # si prefieres st.rerun(), usa esa
                        else:
                            st.error("Contraseña incorrecta.")

        st.markdown("---")
        st.subheader("Registrar usuario")
        with st.form("form_register"):
            r_user = st.text_input("Usuario (nuevo)", placeholder="nuevo.usuario", label_visibility="collapsed")
            r_name = st.text_input("Nombre completo", placeholder="Nombre Apellido", label_visibility="collapsed")
            r_pwd = st.text_input("Contraseña", type="password", placeholder="Crear contraseña", label_visibility="collapsed")
            r_pwd2 = st.text_input("Confirmar contraseña", type="password", placeholder="Confirmar contraseña", label_visibility="collapsed")
            reg = st.form_submit_button("Registrar")
            if reg:
                if not r_user or not r_pwd:
                    st.error("Usuario y contraseña obligatorios.")
                elif r_pwd != r_pwd2:
                    st.error("Las contraseñas no coinciden.")
                elif get_user_by_username(r_user):
                    st.error("Usuario ya existe.")
                else:
                    ok = register_user(r_user, r_pwd, full_name=r_name)
                    if ok:
                        st.success("Usuario registrado. Inicia sesión.")
                    else:
                        st.error("Error al registrar (revisar logs).")

        # link a documentación / ER
        if logo_path:
            st.markdown(f"[Ver ER / Documentación]({logo_path})")

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # panel derecho: ayuda y contactos (más sutil)
        st.markdown('<div style="padding:18px;border-radius:12px;background:rgba(255,255,255,0.01);">', unsafe_allow_html=True)
        st.markdown("**Documentación**")
        if logo_path:
            st.markdown(f"- [ER / Documentación]({logo_path})")
        st.markdown("- Contacto: admin@ejemplo.com")
        st.markdown('</div>', unsafe_allow_html=True)
