# modulos/pages/miembros_page.py

import streamlit as st
from modulos.db.crud_miembros import list_members


def render_miembros():
    st.header("Miembros")

    st.markdown("### Lista de miembros registrados")

    # Intentamos cargar miembros
    try:
        miembros = list_members()
    except Exception as e:
        st.error(f"Error cargando miembros: {e}")
        return

    # Si no hay registros
    if not miembros:
        st.info("No hay miembros registrados todavía.")
        return

    # Mostrar tabla
    st.table(miembros)

    # Mensaje final placeholder
    st.caption("CRUD completo pronto disponible (crear, editar y eliminar).")


