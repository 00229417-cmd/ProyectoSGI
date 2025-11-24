# modulos/pages/ciclo_page.py
import streamlit as st
from modulos.db.crud_ciclo import list_ciclos, create_ciclo

def render_ciclo():
    st.header("📆 Ciclos")
    try:
        rows = list_ciclos()
    except Exception as e:
        st.error(f"Error: {e}")
        rows = []
    st.dataframe(rows, use_container_width=True)

    with st.expander("➕ Crear ciclo"):
        with st.form("form_ciclo", clear_on_submit=True):
            nombre = st.text_input("Nombre ciclo")
            fecha_inicio = st.text_input("Fecha inicio (YYYY-MM-DD)")
            fecha_fin = st.text_input("Fecha fin (YYYY-MM-DD)")
            if st.form_submit_button("Crear"):
                ok = create_ciclo(nombre, fecha_inicio, fecha_fin)
                if ok:
                    st.success("Ciclo creado ✅")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo crear ciclo.")
