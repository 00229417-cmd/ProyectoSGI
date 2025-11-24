# modulos/login.py  (sustituir las funciones _safe_rerun y _render_login_form por estas)

def _safe_rerun():
    """Intenta rerun de forma segura: primero experimental_rerun (si existe), si no -> st.rerun()."""
    try:
        if hasattr(st, "experimental_rerun") and callable(st.experimental_rerun):
            st.experimental_rerun()
            return True
    except Exception:
        pass

    # fallback moderno (st.rerun existe en versiones actuales)
    try:
        if hasattr(st, "rerun") and callable(st.rerun):
            st.rerun()
            return True
    except Exception:
        pass

    return False


def _render_login_form():
    with st.form("login_form_v1", clear_on_submit=False):
        username = st.text_input("Usuario", placeholder="usuario.ejemplo", key="login_user")
        password = st.text_input("Contraseña", type="password", placeholder="********", key="login_pass")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            ok, u_or_msg = verify_user_credentials(username, password)
            if ok:
                user = u_or_msg  # se espera dict con datos del usuario

                # ------------------------
                # Guardar datos de sesión
                # ------------------------
                st.session_state["session_iniciada"] = True
                st.session_state["usuario"] = user.get("username") or user.get("full_name") or username
                st.session_state["user_role"] = user.get("role") or user.get("rol") or "user"

                # Intentamos guardar un identificador numérico en usuario_id.
                # Probamos varias claves posibles que tu CRUD podría devolver:
                possible_id_keys = ["id", "id_administrador", "id_usuario", "usuario_id", "id_user", "id_miembro"]
                usuario_id = None
                for k in possible_id_keys:
                    if k in user and user[k] is not None:
                        usuario_id = user[k]
                        break

                # Si el CRUD devolvió el id como string numérico, convertimos a int si es posible
                if usuario_id is not None:
                    try:
                        # solo convertir si parece un entero
                        if isinstance(usuario_id, str) and usuario_id.isdigit():
                            usuario_id = int(usuario_id)
                        st.session_state["usuario_id"] = usuario_id
                    except Exception:
                        # en caso raro dejamos el valor tal cual (pero es preferible que sea int)
                        st.session_state["usuario_id"] = usuario_id
                else:
                    # No se encontró id en la respuesta; dejar None (mejor setearlo explícitamente)
                    st.session_state["usuario_id"] = None

                # Guarda info opcional para depuración/uso en la app
                st.session_state["usuario_full_name"] = user.get("full_name") or user.get("nombre") or None
                st.session_state["usuario_email"] = user.get("email") or user.get("correo") or None

                st.success(f"Bienvenido {st.session_state['usuario']}!")
                # Forzar rerun de forma segura para que app.py continúe en el siguiente run
                _safe_rerun()
            else:
                st.error(u_or_msg if isinstance(u_or_msg, str) else "Usuario o contraseña incorrecta.")


