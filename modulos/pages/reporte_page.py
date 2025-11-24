# modulos/pages/reporte_page.py
import streamlit as st
from modulos.db.crud_reporte import list_reportes, create_reporte

def render_reporte():
    st.header("📊 Reportes")
    try:
        rows = list_reportes()
    except Exception as e:
        st.error(f"Error: {e}")
        rows = []
    st.dataframe(rows, use_container_width=True)

    with st.expander("➕ Registrar reporte"):
        with st.form("form_reporte", clear_on_submit=True):
            tipo = st.selectbox("Tipo", ["morosidad","movimiento","cierre"])
            usuario = st.text_input("Usuario")
            desc = st.text_area("Descripción")
            if st.form_submit_button("Registrar"):
                ok = create_reporte(tipo, usuario, desc)
                if ok:
                    st.success("Reporte guardado ✅")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo guardar reporte.")
