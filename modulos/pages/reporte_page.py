# modulos/pages/reporte_page.py
import streamlit as st
from modulos.db import crud_reporte
# importamos el helper que permite buscar admins (si el módulo existe)
try:
    from modulos.db import crud_administrador
except Exception:
    crud_administrador = None

def _resolve_admin_input(admin_input: str):
    """
    admin_input puede ser:
      - ID numérico -> devuelve int
      - username / email / nombre completo -> intenta resolver con crud_administrador
    Retorna (id_administrador:int | None, mensaje_error:str|None)
    """
    if admin_input is None or str(admin_input).strip() == "":
        return None, "No se proporcionó administrador."

    # 1) intentar int
    try:
        aid = int(admin_input)
        return aid, None
    except Exception:
        pass

    # 2) intentar resolver por username / email / nombre (si está el crud)
    if crud_administrador:
        admin = crud_administrador.get_by_username_or_email(admin_input)
        if admin:
            # ajustar clave si tu CRUD devuelve otra clave
            return int(admin.get("id_administrador") or admin.get("id") or admin.get("id_admin")), None

    return None, "No se pudo resolver administrador. Ingresa ID numérico o un username/email válido."

def render_reporte():
    st.title("Generar reporte")

    # Tipo de reporte
    tipo = st.selectbox("Tipo de reporte", ["mora", "cierre", "balance"], index=0)

    # ID ciclo opcional: solo aceptar enteros o dejar vacío
    id_ciclo_input = st.text_input("ID ciclo (opcional)", value="", help="Si lo dejas vacío se guardará NULL")
    id_ciclo = None
    if id_ciclo_input.strip() != "":
        try:
            id_ciclo = int(id_ciclo_input)
        except Exception:
            st.warning("ID ciclo debe ser numérico o dejarlo vacío.")
            id_ciclo = None

    # Preferir id desde sesión
    session_admin_id = st.session_state.get("usuario_id") or st.session_state.get("usuario_id_adm") or None

    st.markdown("**Usuario / administrador que genera el reporte**")
    if session_admin_id:
        st.write(f"Usando usuario en sesión (id): **{session_admin_id}**")
        admin_id = session_admin_id
    else:
        admin_input = st.text_input("Usuario/ID administrador (ID numérico, username o email)", value="")
        admin_id, err = _resolve_admin_input(admin_input)
        if err and admin_input:
            st.warning(err)

    descripcion = st.text_area("Descripción (opcional)", value="")

    if st.button("Generar reporte"):
        # validar admin_id
        if not admin_id:
            st.error("No se pudo resolver un id_administrador válido. Guarda el id en la sesión al loguear o ingresa un id numérico o el correo/nombre exacto del administrador.")
            return

        # llamar al CRUD
        ok, msg = crud_reporte.create_reporte(id_ciclo=id_ciclo, id_administrador=int(admin_id), tipo=tipo, descripcion=descripcion or None)
        if ok:
            st.success("Reporte creado y en estado 'pendiente'.")
        else:
            st.error(f"Error creando reporte: {msg}")

# Exponer función principal para app.py
def render_reporte_page():
    render_reporte()

# Para compatibilidad con tu loader que intenta varios nombres:
def render_reporte():
    render_reporte()

