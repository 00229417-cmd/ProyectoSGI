# modulos/login.py
import streamlit as st
from werkzeug.security import check_password_hash

from modulos.db.crud_users import get_user_by_username, create_user

def login_page():
    st.set_page_config(page_title="GAPC - Login", layout="wide")
    # estilos y animación sutil
    st.markdown(
        """
        <style>
        header { visibility: hidden; }
        .center-box { max-width:900px; margin: 10px auto; }
        .logo { width:72px;height:72px;border-radius:12px;background:linear-gradient(135deg,#5b8bff,#3c67d6);display:inline-flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:28px;box-shadow:0 10px 30px rgba(0,0,0,0.45); animation: floaty 6s infinite;}
        @keyframes floaty {0%{transform:translateY(0)}50%{transform:translateY(-6px)}100%{transform:translateY(0)}}
        .title { font-size:28px; color:#F7FBFF; margin-left:14px; display:inline-block; vertical-align:middle;}
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown('<div class="center-box">', unsafe_allow_html=True)
    c1, c2 = st.columns([0.18, 1])
    with c1:
        st.markdown('<div class="logo">G</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="title">GAPC — Portal</div>', unsafe_allow_html=True)
        st.caption("Sistema de Gestión para Grupos de Ahorro y Préstamo Comunitarios")

    st.markdown("---")

    # Login centered
    with st.form("login_form"):
        usuario = st.text_input("Usuario", placeholder="usuario.ejemplo")
        contr = st.text_input("Contraseña", type="password", placeholder="Contraseña")
        col1, col2 = st.columns([0.6, 0.4])
        with col1:
            btn = st.form_submit_button("Entrar")
        with col2:
            reg = st.form_submit_button("Registrar usuario")  # abre registro

        if btn:
            if not usuario or not contr:
                st.warning("Completa usuario y contraseña")
            else:
                u = get_user_by_username(usuario)
                if not u:
                    st.error("Usuario no encontrado")
                else:
                    ph = u.get("password_hash")
                    if ph and check_password_hash(ph, contr):
                        st.session_state["session_iniciada"] = True
                        st.session_state["usuario"] = usuario
                        st.session_state["usuario_id"] = u.get("id")
                        st.session_state["user_role"] = u.get("role")
                        st.success(f"Bienvenido {u.get('full_name') or usuario}!")
                        try:
                            st.experimental_rerun()
                        except Exception:
                            pass
                    else:
                        st.error("Contraseña incorrecta")

        if reg:
            st.session_state["mostrar_registro"] = True

    # Registro (expander)
    if st.session_state.get("mostrar_registro"):
        with st.expander("Registrar usuario"):
            with st.form("registro"):
                r_user = st.text_input("Usuario (nuevo)")
                r_name = st.text_input("Nombre completo")
                r_pwd = st.text_input("Contraseña", type="password")
                r_pwd2 = st.text_input("Confirmar contraseña", type="password")
                if st.form_submit_button("Crear"):
                    if not r_user or not r_pwd:
                        st.error("Usuario y contraseña obligatorios")
                    elif r_pwd != r_pwd2:
                        st.error("Contraseñas no coinciden")
                    elif get_user_by_username(r_user):
                        st.error("Usuario ya existe")
                    else:
                        uid = create_user(r_user, r_pwd, full_name=r_name, role="user")
                        if uid:
                            st.success("Usuario creado, inicia sesión")
                            st.session_state["mostrar_registro"] = False
    st.markdown('</div>', unsafe_allow_html=True)


