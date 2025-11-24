# modulos/pages/reunion_page.py
import streamlit as st
import pandas as pd

def render_reunion():
    st.header("🗓️ Reuniones")
    try:
        from modulos.db import crud_reunion
    except Exception as e:
        st.warning(f"CRUD reunion no encontrado: {e}")
        st.table([])
        return

    try:
        rows = crud_reunion.list_reuniones()
        df = pd.DataFrame(rows) if rows else pd.DataFrame([])
    except Exception as e:
        st.error(f"Error cargando reuniones: {e}")
        df = pd.DataFrame([])

    st.table(df)

