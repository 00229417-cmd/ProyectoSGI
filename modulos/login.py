# modulos/login.py
import streamlit as st
from modulos.db.crud_users import create_user, verify_user_credentials

def _render_login_form():
    st.markdown("<div class='form-wrapper'>", unsafe_allow_html=True)
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Usuario", placeholder="usuario.ejemplo")
        password = st.text_input("Contraseña", type="password", placeholder="********")
        submitted = st.form_submit_button("Entrar")
        if submitted:
            ok, u_or_msg = verify_user_credentials(username, password)
            if ok:
                user = u_or_msg
                st.session_state["session_iniciada"] = True
                st.session_state["usuario"] = user.get("username")
                st.session_state["user_role"] = user.get("role")
                st.success(f"Bienvenido {user.get('full_name') or user.get('username')}!")
                st.experimental_rerun()
            else:
                st.error("Usuario o contraseña incorrecta.")
    st.markdown("</div>", unsafe_allow_html=True)

def _render_register_form():
    st.markdown("### Crear nuevo usuario")
    with st.form("register_form", clear_on_submit=True):
        new_user = st.text_input("Nuevo usuario", placeholder="nuevo.usuario")
        new_name = st.text_input("Nombre completo", placeholder="Nombre Apellido")
        new_email = st.text_input("Correo (opcional)", placeholder="correo@ejemplo.com")
        new_pass = st.text_input("Crear contraseña", type="password")
        new_pass2 = st.text_input("Confirmar contraseña", type="password")
        role = st.selectbox("Rol", ["user", "admin"])
        submit_reg = st.form_submit_button("Registrar")
        if submit_reg:
            if not new_user or not new_pass:
                st.error("Usuario y contraseña son obligatorios.")
                return
            if new_pass != new_pass2:
                st.error("Las contraseñas no coinciden.")
                return
            ok = create_user(new_user, new_pass, full_name=new_name, email=new_email, role=role)
            if ok:
                st.success("Usuario creado correctamente.")
                st.experimental_rerun()
            else:
                st.error("No se pudo crear el usuario (¿username ya existe?).")

def login_page():
    # mostramos el login centrado (usa el card definido en app.py)
    col_left, col_right = st.columns([2,1])
    with col_left:
        _render_login_form()
        # expander como botón de registro: aparece debajo y mantiene la estética
        with st.expander("Registrar usuario", expanded=False):
            _render_register_form()
    with col_right:
        # dejamos la columna derecha limpia para mantener layout y no mostrar textos no deseados
        st.markdown("") 
