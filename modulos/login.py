# modulos/login.py
import streamlit as st
from modulos.db.crud_users import create_user, verify_user_credentials

# ----------------------------------------------------------
# Función segura para ejecutar rerun (sin romper la app)
# ----------------------------------------------------------
def _safe_rerun():
    """Intenta rerun sólo si existe experimental_rerun"""
    try:
        if hasattr(st, "experimental_rerun") and callable(st.experimental_rerun):
            st.experimental_rerun()
            return True
    except Exception:
        import traceback
        traceback.print_exc()
    return False


# ----------------------------------------------------------
# Formulario de LOGIN
# ----------------------------------------------------------
def _render_login_form():
    with st.form("login_form_v1", clear_on_submit=False):
        username = st.text_input("Usuario", placeholder="usuario.ejemplo", key="login_user")
        password = st.text_input("Contraseña", type="password", placeholder="********", key="login_pass")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            ok, u_or_msg = verify_user_credentials(username, password)
            if ok:
                user = u_or_msg
                st.session_state["session_iniciada"] = True
                st.session_state["usuario"] = user.get("username")
                st.session_state["user_role"] = user.get("role")

                st.success(f"Bienvenido {user.get('full_name') or user.get('username')}!")
                _safe_rerun()
            else:
                st.error("Usuario o contraseña incorrecta.")


# ----------------------------------------------------------
# Formulario de REGISTRO (sin login automático)
# ----------------------------------------------------------
def _render_register_form():
    """Renderiza el formulario de registro dentro del expander."""
    with st.form("register_form_v1", clear_on_submit=True):
        st.markdown("### Crear nuevo usuario")

        new_user = st.text_input("Nuevo usuario", placeholder="nuevo.usuario", key="reg_user")
        new_name = st.text_input("Nombre completo", placeholder="Nombre Apellido", key="reg_name")
        new_email = st.text_input("Correo (opcional)", placeholder="correo@ejemplo.com", key="reg_email")

        new_pass = st.text_input("Crear contraseña", type="password", key="reg_pass")
        new_pass2 = st.text_input("Confirmar contraseña", type="password", key="reg_pass2")

        role = st.selectbox("Rol", ["user", "admin"], key="reg_role")

        submit_reg = st.form_submit_button("Registrar")

        if submit_reg:

            # Validaciones básicas
            if not new_user or not new_pass:
                st.error("Usuario y contraseña son obligatorios.")
                return
            if new_pass != new_pass2:
                st.error("Las contraseñas no coinciden.")
                return

            # Crear usuario
            try:
                ok = create_user(
                    new_user,
                    new_pass,
                    full_name=new_name or None,
                    email=new_email or None,
                    role=role
                )
            except Exception:
                import traceback
                traceback.print_exc()
                st.error("Error interno al crear el usuario.")
                return

            # Resultado
            if ok:
                st.success("Usuario creado correctamente. Ya puedes iniciar sesión.")
                _safe_rerun()
            else:
                st.error("No se pudo crear el usuario. ¿Nombre ya existe?")


# ----------------------------------------------------------
# Página principal de LOGIN
# ----------------------------------------------------------
def login_page():
    """
    Página de login centrada con:
      - Formulario de inicio
      - Expander para registro
    """
    left_col, main_col, right_col = st.columns([1, 2, 1])

    with main_col:
        # LOGIN
        _render_login_form()

        st.markdown("---")

        # REGISTRO (expander debajo del login)
        with st.expander("Registrar usuario", expanded=False):
            _render_register_form()

    # columnas laterales vacías para mantener el diseño centrado
    with left_col:
        st.markdown("")
    with right_col:
        st.markdown("")


