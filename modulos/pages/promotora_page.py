# modulos/pages/promotora_page.py
import streamlit as st
from modulos.db.crud_promotora import list_promotoras, create_promotora

def render_promotora():
    st.header("👥 Promotoras / Organizaciones")
    try:
        rows = list_promotoras()
    except Exception as e:
        st.error(f"Error: {e}")
        rows = []
    st.dataframe(rows, use_container_width=True)

    with st.expander("➕ Nueva promotora"):
        with st.form("form_promotora", clear_on_submit=True):
            nombre = st.text_input("Nombre")
            contacto = st.text_input("Contacto")
            if st.form_submit_button("Crear"):
                ok = create_promotora(nombre, contacto)
                if ok:
                    st.success("Promotora creada ✅")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo crear promotora.")
