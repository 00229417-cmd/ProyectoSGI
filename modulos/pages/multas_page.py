# modulos/pages/multas_page.py
import streamlit as st
from modulos.db.crud_multas import list_multas, create_multa

def render_multas():
    st.header("⚠️ Multas")
    try:
        rows = list_multas()
    except Exception as e:
        st.error(f"Error: {e}")
        rows = []
    st.dataframe(rows, use_container_width=True)

    with st.expander("➕ Registrar multa"):
        with st.form("form_multa", clear_on_submit=True):
            id_miembro = st.number_input("ID miembro", min_value=1, value=1)
            id_reunion = st.number_input("ID reunión (opcional)", min_value=0, value=0)
            monto = st.number_input("Monto", min_value=0.0, format="%.2f")
            motivo = st.text_input("Motivo")
            if st.form_submit_button("Registrar multa"):
                ok = create_multa(id_miembro, id_reunion if id_reunion>0 else None, monto, motivo)
                if ok:
                    st.success("Multa registrada ✅")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo registrar la multa.")
