# modulos/pages/asistencia_page.py
import streamlit as st
from modulos.db.crud_asistencia import list_asistencias, record_asistencia

def render_asistencia():
    st.header("🪑 Asistencia")
    try:
        rows = list_asistencias()
    except Exception as e:
        st.error(f"Error: {e}")
        rows = []
    st.dataframe(rows, use_container_width=True)

    with st.expander("Registrar asistencia"):
        with st.form("form_asistencia", clear_on_submit=True):
            id_reunion = st.number_input("ID reunión", min_value=1, value=1)
            id_miembro = st.number_input("ID miembro", min_value=1, value=1)
            presente = st.checkbox("Presente", value=True)
            obs = st.text_input("Observaciones")
            if st.form_submit_button("Registrar"):
                ok = record_asistencia(id_reunion, id_miembro, presente, obs)
                if ok:
                    st.success("Asistencia registrada ✅")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo registrar asistencia.")
