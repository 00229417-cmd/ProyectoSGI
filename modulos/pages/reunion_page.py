# modulos/pages/reunion_page.py
import streamlit as st
from modulos.db.crud_reunion import list_reuniones, create_reunion

def render_reunion():
    st.header("📅 Reuniones")
    try:
        rows = list_reuniones()
    except Exception as e:
        st.error(f"Error: {e}")
        rows = []
    st.dataframe(rows, use_container_width=True)

    with st.expander("➕ Crear reunión"):
        with st.form("form_reunion", clear_on_submit=True):
            id_ciclo = st.number_input("ID ciclo", min_value=1, value=1)
            fecha = st.text_input("Fecha (YYYY-MM-DD)")
            lugar = st.text_input("Lugar")
            desc = st.text_area("Descripción")
            if st.form_submit_button("Crear reunión"):
                ok = create_reunion(id_ciclo, fecha, lugar, desc)
                if ok:
                    st.success("Reunión creada ✅")
                    st.experimental_rerun()
                else:
                    st.error("Error al crear reunión.")
