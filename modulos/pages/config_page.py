# modulos/pages/config_page.py
import streamlit as st
import json
import os
from datetime import datetime
from typing import Any

# -----------------------
# Helpers
# -----------------------
def _safe_rerun():
    try:
        if hasattr(st, "experimental_rerun") and callable(st.experimental_rerun):
            st.experimental_rerun()
            return
    except Exception:
        pass
    try:
        if hasattr(st, "rerun") and callable(st.rerun):
            st.rerun()
            return
    except Exception:
        pass

def _load_json_settings(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_json_settings(path: str, obj: dict) -> bool:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

# Rutas de fallback
FALLBACK_SETTINGS_PATH = os.environ.get("FALLBACK_SETTINGS_PATH", "data/settings.json")

# -----------------------
# Intentar importar CRUDs (si existen)
# -----------------------
crud_users = None
crud_logs = None
crud_settings = None

try:
    from modulos.db import crud_users as crud_users  # tipo: ignore
except Exception:
    crud_users = None

try:
    from modulos.db import crud_logs as crud_logs  # tipo: ignore
except Exception:
    crud_logs = None

try:
    from modulos.db import crud_settings as crud_settings  # tipo: ignore
except Exception:
    crud_settings = None

# -----------------------
# Renderers independientes
# -----------------------
def _render_profile_section(user_id: Any):
    st.subheader("Perfil")
    if user_id is None:
        st.warning("No hay usuario identificado en sesión. Inicia sesión para ver/editar tu perfil.")
        return

    # intentar obtener usuario desde CRUD
    user = None
    if crud_users:
        try:
            # se asume que existe una función obtener_usuario(id) o get_user
            if hasattr(crud_users, "obtener_usuario"):
                user = crud_users.obtener_usuario(user_id)
            elif hasattr(crud_users, "get_user"):
                user = crud_users.get_user(user_id)
            elif hasattr(crud_users, "get_user_by_id"):
                user = crud_users.get_user_by_id(user_id)
        except Exception as e:
            st.error(f"Error al obtener usuario desde DB: {e}")

    # fallback: si crud_users no existe o no devolvió, usar sesión
    if not user:
        user = {
            "id": st.session_state.get("usuario_id"),
            "username": st.session_state.get("usuario"),
            "full_name": st.session_state.get("usuario_full_name"),
            "email": st.session_state.get("usuario_email"),
            "role": st.session_state.get("user_role"),
        }

    with st.form("form_perfil"):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Usuario (username)", value=user.get("username") or "", disabled=True)
            fullname = st.text_input("Nombre completo", value=user.get("full_name") or "")
        with col2:
            email = st.text_input("Correo", value=user.get("email") or "")
            role = st.text_input("Rol (solo lectura)", value=str(user.get("role") or ""), disabled=True)

        submitted = st.form_submit_button("Guardar cambios perfil")
        if submitted:
            if crud_users and hasattr(crud_users, "update_user"):
                try:
                    # intento de API común: update_user(id, data_dict) o update_user(id, fullname, email)
                    if hasattr(crud_users, "update_user"):
                        try:
                            crud_users.update_user(user_id, {"full_name": fullname, "email": email})
                        except TypeError:
                            # fallback positional
                            crud_users.update_user(user_id, fullname, email)
                    st.success("Perfil actualizado.")
                    _safe_rerun()
                except Exception as e:
                    st.error(f"Error guardando en DB: {e}")
            else:
                st.info("No hay soporte DB para actualizar perfil. Se actualizarán los valores en la sesión (temporal).")
                st.session_state["usuario"] = username
                st.session_state["usuario_full_name"] = fullname
                st.session_state["usuario_email"] = email
                st.success("Valores actualizados en sesión.")
                _safe_rerun()

def _render_password_section(user_id: Any):
    st.subheader("Cambiar contraseña")
    with st.form("form_pass"):
        current = st.text_input("Contraseña actual", type="password")
        newpass = st.text_input("Nueva contraseña", type="password")
        newpass2 = st.text_input("Confirmar nueva contraseña", type="password")
        submit = st.form_submit_button("Cambiar contraseña")

        if submit:
            if not newpass or newpass != newpass2:
                st.error("Las contraseñas no coinciden o están vacías.")
                return
            if not user_id:
                st.error("No hay usuario identificado en sesión.")
                return

            if crud_users and hasattr(crud_users, "change_password"):
                try:
                    ok = crud_users.change_password(user_id, current, newpass)
                    if ok:
                        st.success("Contraseña cambiada correctamente.")
                    else:
                        st.error("No se cambió la contraseña. Verifica la contraseña actual.")
                except Exception as e:
                    st.error(f"Error cambiando la contraseña: {e}")
            else:
                st.info("Función de cambio de contraseña no disponible en CRUD. Implementa `crud_users.change_password(user_id, current, new)`.")
                # opción de fallback: no hacemos nada por seguridad

def _render_role_management():
    st.subheader("Administrar roles (solo administradores)")
    if st.session_state.get("user_role") != "admin":
        st.info("Solo usuarios con rol 'admin' pueden ver esta sección.")
        return

    if crud_users and hasattr(crud_users, "list_users"):
        try:
            users = crud_users.list_users()
        except Exception as e:
            st.error(f"Error recuperando usuarios: {e}")
            users = []
    else:
        st.info("No hay CRUD de usuarios disponible. Implementa `crud_users.list_users()` para habilitar administración de roles.")
        users = []

    if not users:
        st.write("No hay usuarios para mostrar.")
        return

    # mostra tabla y permitir cambiar rol
    try:
        import pandas as pd
        df = pd.DataFrame(users)
        # mostrar tabla con columnas mínimas
        st.dataframe(df[["id", "username", "full_name", "email", "role"]] if "id" in df.columns else df)
    except Exception:
        st.write(users)

    st.markdown("---")
    with st.form("form_roles"):
        uid = st.selectbox("Selecciona usuario", options=[u.get("id") for u in users], format_func=lambda v: next((x.get("username") for x in users if x.get("id")==v), str(v)))
        newrole = st.selectbox("Nuevo rol", ["user", "admin", "manager", "viewer"])
        sub = st.form_submit_button("Actualizar rol")
        if sub:
            try:
                if hasattr(crud_users, "update_role"):
                    crud_users.update_role(uid, newrole)
                    st.success("Rol actualizado.")
                    _safe_rerun()
                elif hasattr(crud_users, "update_user"):
                    # intentar usando update_user
                    crud_users.update_user(uid, {"role": newrole})
                    st.success("Rol actualizado (vía update_user).")
                    _safe_rerun()
                else:
                    st.error("No existe función conocida para actualizar rol. Implementa `update_role` o `update_user` en crud_users.")
            except Exception as e:
                st.error(f"Error al actualizar rol: {e}")

def _render_logs_section():
    st.subheader("Logs de actividad")
    if crud_logs and hasattr(crud_logs, "list_logs"):
        try:
            logs = crud_logs.list_logs(limit=200)
        except Exception as e:
            st.error(f"Error obteniendo logs desde DB: {e}")
            logs = []
    else:
        st.info("No existe crud_logs con `list_logs`. Puedes crear `modulos.db.crud_logs` o revisar la tabla `activity_logs` en tu DB.")
        logs = []

    if not logs:
        st.write("No hay logs para mostrar.")
        return

    try:
        import pandas as pd
        df = pd.DataFrame(logs)
        st.dataframe(df)
    except Exception:
        st.write(logs)

def _render_system_options():
    st.subheader("Opciones del sistema")
    st.markdown("Estas opciones se guardan en **BD** si `crud_settings` está disponible, si no en un archivo local `data/settings.json` (fallback).")

    # cargar settings
    settings = {}
    if crud_settings and hasattr(crud_settings, "get_settings"):
        try:
            settings = crud_settings.get_settings()
        except Exception:
            settings = {}
    else:
        settings = _load_json_settings(FALLBACK_SETTINGS_PATH)

    # mostrar y editar
    with st.form("form_settings"):
        currency = st.text_input("Moneda", value=settings.get("currency", "USD"))
        max_loan = st.number_input("Límite máximo de préstamo por miembro", value=float(settings.get("max_loan", 10000.0)))
        default_interest = st.number_input("Tasa de interés (%) por defecto", value=float(settings.get("default_interest", 5.0)))
        allow_anonymous_reports = st.checkbox("Permitir reportes anónimos", value=bool(settings.get("allow_anonymous_reports", False)))
        submit = st.form_submit_button("Guardar opciones del sistema")

        if submit:
            new_settings = {
                "currency": currency,
                "max_loan": float(max_loan),
                "default_interest": float(default_interest),
                "allow_anonymous_reports": bool(allow_anonymous_reports),
                "updated_at": datetime.utcnow().isoformat(),
            }
            if crud_settings and hasattr(crud_settings, "save_settings"):
                try:
                    crud_settings.save_settings(new_settings)
                    st.success("Opciones guardadas en DB.")
                    _safe_rerun()
                except Exception as e:
                    st.error(f"Error guardando en DB: {e}")
            else:
                ok = _save_json_settings(FALLBACK_SETTINGS_PATH, new_settings)
                if ok:
                    st.success(f"Opciones guardadas en {FALLBACK_SETTINGS_PATH}.")
                    _safe_rerun()
                else:
                    st.error("No se pudo guardar opciones.")

# -----------------------
# Render principal
# -----------------------
def render_config():
    st.title("⚙️ Configuración")

    st.markdown("### Tipos de configuraciones disponibles")
    st.markdown(
        "- Perfil personal (editar nombre / correo)\n"
        "- Cambiar contraseña\n"
        "- Administrar roles (solo `admin`)\n"
        "- Ver logs de actividad\n"
        "- Opciones del sistema (moneda, tasas, límites)\n"
    )

    st.divider()
    user_id = st.session_state.get("usuario_id")

    # Secciones
    _render_profile_section(user_id)
    st.markdown("---")
    _render_password_section(user_id)
    st.markdown("---")
    _render_role_management()
    st.markdown("---")
    _render_logs_section()
    st.markdown("---")
    _render_system_options()
    st.markdown("---")

 
