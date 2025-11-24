# modulos/pages/reporte_page.py

import streamlit as st

# Importación directa y correcta de los CRUD
from modulos.db.crud_reporte import list_reportes, create_reporte
from modulos.db.crud_ciclo import list_ciclos
from modulos.db.crud_administrador import list_administradores


def render_reporte():
    st.header("📄 Reportes")

    # =====================
    # LISTADO DE REPORTES
    # =====================
    try:
        reportes = list_reportes()
        st.subheader("Listado")
        st.table(reportes)
    except Exception as e:
        st.error(f"Error cargando reportes: {e}")

    st.divider()

    # =====================
    # CREAR REPORTE
    # =====================
    st.subheader("Crear reporte")

    try:
        ciclos = list_ciclos()
        ciclo_ids = [c["id_ciclo"] for c in ciclos]
    except:
        ciclo_ids = []

    tipo = st.selectbox("Tipo de reporte", ["mora", "morosidad", "prestamos", "aportes"])

    usuario = st.text_input("Usuario que genera el reporte")

    desc = st.text_area("Descripción (opcional)")

    if st.button("Crear reporte"):
        try:
            ok = create_reporte(tipo=tipo, usuario=usuario, descripcion=desc)
            if ok:
                st.success("Reporte creado correctamente.")
                st.rerun()  # CORRECTO: reemplaza experimental_rerun
        except Exception as e:
            st.error(f"Error creando reporte: {e}")



