# modulos/login.py
import streamlit as st
from modulos.db.crud_users import create_user, verify_user_credentials

def _safe_rerun():
    """
    Llama a st.experimental_rerun() de forma segura (si existe).
    Devuelve True si realizó rerun, False en caso contrario.
    """
    try:
        if hasattr(st, "experimental_rerun") and callable(st.experimental_rerun):
            st.experimental_rerun()
            return True
    except Exception:
        # no romper la app si rerun falla; imprimir traza en logs
        import traceback
        traceback.print_exc()
    return False

def _render_login_form():
    """Formulario de inicio de sesión (dentro de un st.form)"""
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
                # recargar para que la app muestre la interfaz principal (de forma segura)
                _safe_rerun()
            else:
                # u_or_msg puede ser mensaje de error
                st.error("Usuario o contraseña incorrecta.")

def _render_register_form():
    """Formulario de registro (dentro de st.form). Al registrarse inicia sesión automáticamente."""
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
            # validaciones mínimas
            if not new_user or not new_pass:
                st.error("Usuario y contraseña son obligatorios.")
                return
            if new_pass != new_pass2:
                st.error("Las contraseñas no coinciden.")
                return

            # intentar crear el usuario (manejo de excepciones dentro)
            try:
                ok = create_user(new_user, new_pass, full_name=new_name or None, email=new_email or None, role=role)
            except Exception:
                import traceback
                traceback.print_exc()
                st.error("Ocurrió un error interno al crear el usuario. Revisa los logs.")
                return

            if ok:
                # iniciar sesión automáticamente con el nuevo usuario
                st.session_state["session_iniciada"] = True
                st.session_state["usuario"] = new_user
                st.session_state["user_role"] = role
                st.success("Usuario creado correctamente. Iniciando sesión...")
                # intentar rerun de forma segura; si no funciona, informar al usuario
                did_rerun = _safe_rerun()
                if not did_rerun:
                    st.info("Usuario creado. Refresca la página para ver la interfaz principal si no se redirige automáticamente.")
                return
            else:
                st.error("No se pudo crear el usuario. Verifica que el nombre de usuario no exista.")

def login_page():
    """
    Página de login con:
      - formulario de login (centrado)
      - expander 'Registrar usuario' debajo (un solo click para abrir/llenar/registrar)
    """
    # columnas para centrar: columna central (2) y márgenes a los lados (1 y 1)
    left_col, main_col, right_col = st.columns([1, 2, 1])

    with main_col:
        # login (centrado en la columna principal)
        _render_login_form()

        st.markdown("---")

        # expander: un sólo click para mostrar registro
        with st.expander("Registrar usuario", expanded=False):
            _render_register_form()

    # derecha e izquierda vacías para respetar el layout
    with left_col:
        st.markdown("") 
    with right_col:
        st.markdown("")



