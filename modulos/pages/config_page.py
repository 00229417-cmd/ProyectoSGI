# modulos/pages/config_page.py
import streamlit as st
from modulos.db.crud_config import list_tipo_usuario

def render_config():
    st.header("⚙️ Configuración")
    st.subheader("Tipos de usuario")
    try:
        rows = list_tipo_usuario()
    except Exception as e:
        st.error(f"Error: {e}")
        rows = []
    st.dataframe(rows, use_container_width=True)
    st.info("Aquí puedes añadir más opciones de configuración según necesites.")
