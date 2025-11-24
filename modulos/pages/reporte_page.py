# modulos/pages/reporte_page.py
import streamlit as st
from sqlalchemy import text
from modulos.config.conexion import get_engine
from modulos.db import crud_reporte

def _resolve_admin_to_id(candidate: str | int) -> int | None:
    """
    Intenta convertir candidate a entero.
    Si no es entero, busca en la tabla administrador por correo/nombre/apellido.
    Devuelve id_administrador (int) o None si no encuentra.
    """
    if candidate is None or candidate == "":
        return None
    # si ya es entero
    try:
        return int(candidate)
    except Exception:
        pass

    # buscar en BD
    try:
        engine = get_engine()
        with engine.connect() as conn:
            q = text("""
                SELECT id_administrador
                FROM administrador
                WHERE correo = :v OR nombre = :v OR apellido = :v
                LIMIT 1
            """)
            r = conn.execute(q, {"v": candidate}).fetchone()
            if r:
                try:
                    return int(r[0])
                except Exception:
                    return None
    except Exception as e:
        st.error(f"Error resolviendo administrador: {e}")
        return None

def render_reporte():
    st.header("Generar reporte")

    with st.form("form_reporte"):
        tipo = st.selectbox("Tipo de reporte", ["mora", "cierre", "balance", "morosidad"])
        id_ciclo = st.text_input("ID ciclo (opcional)", value="")
        usuario_input = st.text_input("Usuario/ID administrador", value=st.session_state.get("usuario",""))
        descripcion = st.text_area("Descripción (opcional)", value="")
        submitted = st.form_submit_button("Crear reporte")

    if not submitted:
        return

    # 1) prioridad: usar id guardado en sesión (recomendado)
    id_admin_session = st.session_state.get("usuario_id")
    if id_admin_session:
        id_adm_param = id_admin_session
    else:
        # 2) si no hay id en sesión, resolver el texto que el usuario ingresó
        id_adm_param = _resolve_admin_to_id(usuario_input)

    if id_adm_param is None:
        st.error("No se pudo resolver un id_administrador válido. Guarda el id en la sesión al loguear o ingresa un id numérico o el correo/nombre exacto del administrador.")
        return

    # Llamada al CRUD (crud_reporte.create_reporte debe aceptar id_adm int o hacer su propia validación)
    res = crud_reporte.create_reporte(id_ciclo, id_adm_param, tipo, descripcion)
    if res.get("ok"):
        st.success(f"Reporte creado correctamente. id = {res.get('id')}")
    else:
        st.error(f"Error creando reporte: {res.get('msg')}")
