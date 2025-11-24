# modulos/pages/cierre_page.py
import streamlit as st
from modulos.db.crud_cierre import list_cierres, create_cierre

def render_cierre():
    st.header("🔒 Cierre de ciclo")
    try:
        rows = list_cierres()
    except Exception as e:
        st.error(f"Error: {e}")
        rows = []
    st.dataframe(rows, use_container_width=True)

    with st.expander("➕ Generar cierre"):
        with st.form("form_cierre", clear_on_submit=True):
            id_ciclo = st.number_input("ID ciclo", min_value=1, value=1)
            resumen = st.text_area("Resumen / observaciones")
            if st.form_submit_button("Generar cierre"):
                ok = create_cierre(id_ciclo, resumen)
                if ok:
                    st.success("Cierre generado ✅")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo generar cierre.")
