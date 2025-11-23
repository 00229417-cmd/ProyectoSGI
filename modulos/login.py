# modulos/login.py
import streamlit as st
from modulos.db.crud_users import create_user, verify_user_credentials

def _render_login_form():
    """Formulario de inicio de sesión (dentro de un st.form)"""
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
                # recargar para que la app muestre la interfaz principal
                st.experimental_rerun()
            else:
                st.error("Usuario o contraseña incorrecta.")

def _render_register_form():
    """Formulario de registro (dentro de expander). Al registrarse hace rerun para cerrar expander"""
    with st.form("register_form", clear_on_submit=True):
        st.markdown("### Crear nuevo usuario")
        new_user = st.text_input("Nuevo usuario", placeholder="nuevo.usuario")
        new_name = st.text_input("Nombre completo", placeholder="Nombre Apellido")
        new_email = st.text_input("Correo (opcional)", placeholder="correo@ejemplo.com")
        new_pass = st.text_input("Crear contraseña", type="password")
        new_pass2 = st.text_input("Confirmar contraseña", type="password")
        role = st.selectbox("Rol", ["user", "admin"])
        submit_reg = st.form_submit_button("Registrar")
        if submit_reg:
            # validaciones mínimas
            if not new_user or not new_pass:
                st.error("Usuario y contraseña son obligatorios.")
                return
            if new_pass != new_pass2:
                st.error("Las contraseñas no coinciden.")
                return
            ok = create_user(new_user, new_pass, full_name=new_name, email=new_email, role=role)
            if ok:
                st.success("Usuario creado correctamente.")
                # recarga para evitar doble-submit y para que el expander aparezca cerrado
                st.experimental_rerun()
            else:
                st.error("No se pudo crear el usuario (¿username ya existe?).")

def login_page():
    """
    Página de login con:
      - formulario de login (centrado)
      - expander 'Registrar usuario' debajo (sin botón modal)
    """
    # columnas para centrar: columna central (2) y márgenes a los lados (1 y 1)
    left_col, main_col, right_col = st.columns([1, 2, 1])

    with main_col:
        # login (centrado en la columna principal)
        _render_login_form()

        st.markdown("---")

        # expander: solo uno click para abrir/llenar/registrar
        with st.expander("Registrar usuario", expanded=False):
            _render_register_form()

    # derecha e izquierda vacías para respetar el layout
    with left_col:
        st.markdown("") 
    with right_col:
        st.markdown("")


