# modulos/pages/reporte_page.py
import streamlit as st
from modulos.db import crud_reporte, crud_ciclo, crud_administrador

def render_reporte():
    st.header("📄 Reportes")

    # obtén ciclos y administradores para selectboxes
    try:
        ciclos = crud_ciclo.list_ciclos()  # debe devolver list[dict] con id_ciclo, fecha_inicio...
    except Exception:
        ciclos = []

    try:
        admins = crud_administrador.list_administradores()  # list[dict] con id_administrador, nombre, correo...
    except Exception:
        admins = []

    # opciones para tipo de reporte
    tipos = ["mora", "cierre", "balance", "morosidad", "otros"]

    with st.form("form_reporte"):
        col1, col2 = st.columns(2)
        with col1:
            # select de ciclo (incluye opción 'Ninguno')
            ciclo_options = [("— Ninguno —", None)] + [
                (f"{c.get('id_ciclo')} — {c.get('fecha_inicio') or ''}", c.get("id_ciclo")) for c in ciclos
            ]
            ciclo_choice = st.selectbox("Ciclo (opcional)", [t[0] for t in ciclo_options])
            # extraer id del choice
            idx = [t[0] for t in ciclo_options].index(ciclo_choice)
            id_ciclo = ciclo_options[idx][1]

            tipo = st.selectbox("Tipo de reporte", tipos, index=0)
            descripcion = st.text_area("Descripción (opcional)")

        with col2:
            admin_options = [("— Usuario actual —", None)] + [
                (f"{a.get('id_administrador')} — {a.get('nombre') or a.get('correo')}", a.get("id_administrador")) for a in admins
            ]
            admin_choice = st.selectbox("Administrador (opcional)", [t[0] for t in admin_options])
            idx2 = [t[0] for t in admin_options].index(admin_choice)
            id_administrador = admin_options[idx2][1]

            st.write("")  # espacio
            submitted = st.form_submit_button("Generar reporte")

        if submitted:
            # llama a create_reporte con parámetros en el orden correcto
            ok, msg = crud_reporte.create_reporte(
                id_ciclo=id_ciclo, 
                id_administrador=id_administrador, 
                tipo=tipo, 
                descripcion=descripcion
            )

            if ok:
                st.success(msg or "Reporte creado (pendiente).")
            else:
                st.error(f"Error creando reporte: {msg}")
