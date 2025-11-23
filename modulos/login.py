# modulos/login.py
import streamlit as st
from modulos.db.crud_users import create_user, verify_user_credentials, get_user_by_username

# inicializar flag en session_state
if "show_register" not in st.session_state:
    st.session_state["show_register"] = False

def _render_login_form():
    st.markdown("## Iniciar sesión")
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
                # recargar para mostrar la app principal
                st.experimental_rerun()
            else:
                st.error("Usuario o contraseña incorrecta.")

def _render_register_form():
    st.markdown("### Registrar usuario")
    with st.form("register_form", clear_on_submit=True):
        new_user = st.text_input("Nuevo usuario", placeholder="nuevo.usuario")
        new_name = st.text_input("Nombre completo", placeholder="Nombre Apellido")
        new_email = st.text_input("Correo (opcional)", placeholder="correo@ejemplo.com")
        new_pass = st.text_input("Crear contraseña", type="password")
        new_pass2 = st.text_input("Confirmar contraseña", type="password")
        role = st.selectbox("Rol", ["user", "admin"])
        submit_reg = st.form_submit_button("Registrar")
        if submit_reg:
            # validaciones básicas
            if not new_user or not new_pass:
                st.error("Usuario y contraseña son obligatorios.")
                return
            if new_pass != new_pass2:
                st.error("Las contraseñas no coinciden.")
                return
            ok = create_user(new_user, new_pass, full_name=new_name, email=new_email, role=role)
            if ok:
                st.success("Usuario creado correctamente.")
                # opcional: ocultar formulario tras creación
                st.session_state["show_register"] = False
                # forzar recarga para evitar reenvío del form
                st.experimental_rerun()
            else:
                st.error("No se pudo crear el usuario (¿username ya existe?).")

def login_page():
    """
    Página de login: muestra formulario de login y un botón 'Registrar usuario' debajo.
    Al pulsar el botón se despliega el formulario de registro.
    """
    # usamos una fila principal + columna derecha vacía (para mantener layout similar)
    col_main, col_empty = st.columns([2, 1])

    with col_main:
        _render_login_form()

        # espacio / separador estético
        st.markdown("---")

        # Botón que alterna la visualización del formulario de registro
        # (se mantiene la apariencia original del resto)
        if st.button("Registrar usuario"):
            # alternar estado
            st.session_state["show_register"] = not st.session_state["show_register"]

        # mostrar el formulario SOLO si el flag está activo
        if st.session_state["show_register"]:
            _render_register_form()

    # Columna derecha intencionalmente vacía (no mostrar texto "Información")
    with col_empty:
        st.markdown("")  # mantiene el layout sin contenido visible
