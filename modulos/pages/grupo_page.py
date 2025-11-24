# modulos/pages/grupo_page.py
import streamlit as st
from modulos.db.crud_grupo import list_grupos, create_grupo

def render_grupo():
    st.header("🔗 Grupos")
    try:
        rows = list_grupos()
    except Exception as e:
        st.error(f"Error: {e}")
        rows = []
    st.dataframe(rows, use_container_width=True)

    with st.expander("➕ Crear grupo"):
        with st.form("form_grupo", clear_on_submit=True):
            nombre = st.text_input("Nombre del grupo")
            desc = st.text_area("Descripción")
            if st.form_submit_button("Crear"):
                ok = create_grupo(nombre, desc)
                if ok:
                    st.success("Grupo creado ✅")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo crear grupo.")
