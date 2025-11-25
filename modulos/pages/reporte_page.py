# modulos/pages/reporte_page.py
import streamlit as st
from modulos.db import crud_reporte

# intentar cargar CRUD administrador si existe
try:
    from modulos.db import crud_administrador
except Exception:
    crud_administrador = None


def resolve_admin_input(admin_input: str):
    """
    admin_input puede ser:
        - un ID numérico
        - un username / email si crud_administrador existe
    Devuelve: (admin_id, error)
    """
    if admin_input is None or admin_input.strip() == "":
        return None, "No se proporcionó administrador."

    # 1) intentar convertir a entero
    try:
        return int(admin_input), None
    except:
        pass

    # 2) intentar buscar por username/email
    if crud_administrador:
        try:
            adm = crud_administrador.get_by_username_or_email(admin_input)
            if adm:
                return (
                    adm.get("id_administrador")
                    or adm.get("id")
                    or adm.get("id_admin"),
                    None
                )
        except:
            pass

    return None, "No se pudo resolver administrador. Ingresa un ID numérico válido."


def render_reporte():
    st.title("📄 Generar reporte")

    # ================================
    # TIPO DE REPORTE
    # ================================
    tipo = st.selectbox("Tipo de reporte", ["mora", "cierre", "balance"])

    # ================================
    # CICLO
    # ================================
    id_ciclo_input = st.text_input("ID ciclo (opcional)", value="")
    id_ciclo = None

    # convertir si viene algo
    if id_ciclo_input.strip() != "":
        try:
            id_ciclo = int(id_ciclo_input)
        except:
            st.warning("⚠️ ID ciclo debe ser numérico o dejarlo vacío.")
            id_ciclo = None

    # ================================
    # ADMINISTRADOR
    # ================================
    session_admin_id = (
        st.session_state.get("usuario_id")
        or st.session_state.get("usuario_id_adm")
        or None
    )

    st.markdown("**Usuario / administrador que genera el reporte**")

    if session_admin_id:
        st.success(f"Usando ID administrador desde sesión: **{session_admin_id}**")
        admin_id = session_admin_id
        manual_input = None
    else:
        manual_input = st.text_input("ID administrador (numérico)", value="")
        admin_id, err = resolve_admin_input(manual_input)
        if err and manual_input.strip():
            st.warning(err)

    descripcion = st.text_area("Descripción (opcional)", value="")

    # ================================
    # BOTÓN GUARDAR
    # ================================
    if st.button("Crear reporte"):
        if not admin_id:
            st.error("No se pudo obtener un ID administrador válido.")
            return

        ok, msg = crud_reporte.create_reporte(
            id_ciclo=id_ciclo,
            id_administrador=int(admin_id),
            tipo=tipo,
            descripcion=descripcion or None
        )

        if ok:
            st.success("Reporte creado correctamente ✔️")
        else:
            st.error(f"Error creando reporte: {msg}")


# para compatibilidad con loader del app.py
def render_reporte_page():
    render_reporte()

