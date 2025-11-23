# modulos/login.py
import streamlit as st
from modulos.db.crud_users import create_user, verify_user_credentials

def _safe_rerun():
    """Llamar a experimental_rerun si está disponible."""
    try:
        if hasattr(st, "experimental_rerun") and callable(st.experimental_rerun):
            st.experimental_rerun()
            return True
    except Exception:
        pass
    return False


def _render_login_form():
    """
    Formulario de login con comportamiento:
     - Si se hace submit y credenciales ok -> set session + rerun inmediato y RETURN
     - Si no ok -> mostrar error y quedarse en login
    """
    with st.form("login_form_v1", clear_on_submit=False):
        username = st.text_input("Usuario", placeholder="usuario.ejemplo", key="login_user")
        password = st.text_input("Contraseña", type="password", placeholder="********", key="login_pass")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            try:
                ok, u_or_msg = verify_user_credentials(username, password)
            except Exception as e:
                st.error("Error al verificar credenciales.")
                return

            if ok:
                user = u_or_msg
                # --- marcar sesión inmediatamente ---
                st.session_state["session_iniciada"] = True
                st.session_state["usuario"] = user.get("username")
                st.session_state["user_role"] = user.get("role")

                # mensaje rápido (opcional)
                st.success(f"Bienvenido {user.get('full_name') or user.get('username')}!")

                # Forzamos rerun y retornamos para evitar que el mismo run siga renderizando el formulario.
                _safe_rerun()
                return
            else:
                st.error("Usuario o contraseña incorrecta.")


def _render_register_form():
    """
    Formulario registro dentro de expander.
    No hace login automático; sólo crea el usuario y recarga para cerrar el expander.
    """
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
            if not new_user or not new_pass:
                st.error("Usuario y contraseña son obligatorios.")
                return
            if new_pass != new_pass2:
                st.error("Las contraseñas no coinciden.")
                return

            try:
                ok = create_user(new_user, new_pass, full_name=new_name or None, email=new_email or None, role=role)
            except Exception:
                st.error("Error interno al crear el usuario.")
                return

            if ok:
                st.success("Usuario creado correctamente. Ya puedes iniciar sesión.")
                # recarga para cerrar expander
                _safe_rerun()
                return
            else:
                st.error("No se pudo crear el usuario. ¿Nombre ya existe?")


def login_page():
    """
    Página de login centrada con:
      - Formulario de inicio
      - Expander 'Registrar usuario' debajo
    Si la sesión ya está iniciada -> retornar sin renderizar nada.
    """
    # Si ya está iniciada la sesión, no mostramos el login (esto evita que se vea tras rerun)
    if st.session_state.get("session_iniciada"):
        return

    left_col, main_col, right_col = st.columns([1, 2, 1])

    with main_col:
        # Render login form. Si el usuario hace login con éxito, la función _render_login_form
        # hará un rerun y retornará sin que el resto del page siga.
        _render_login_form()

        # Si, por alguna razón, la sesión fue activada dentro del mismo run y no se produjo rerun,
        # comprobamos aquí y salimos inmediatamente (previene mostrar el expander después de login).
        if st.session_state.get("session_iniciada"):
            return

        st.markdown("---")

        # Expander de registro (debajo)
        with st.expander("Registrar usuario", expanded=False):
            _render_register_form()

    # columnas laterales vacías para mantener el diseño centrado
    with left_col:
        st.markdown("")
    with right_col:
        st.markdown("")



