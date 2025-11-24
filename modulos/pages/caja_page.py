# modulos/pages/caja_page.py
import streamlit as st
import pandas as pd

def render_caja():
    st.header("🧾 Caja")
    try:
        from modulos.db import crud_caja
    except Exception as e:
        st.warning(f"CRUD caja no encontrado: {e}")
        st.table([])
        return

    try:
        rows = crud_caja.list_caja()
        df = pd.DataFrame(rows) if rows else pd.DataFrame([])
    except Exception as e:
        st.error(f"Error cargando caja: {e}")
        df = pd.DataFrame([])

    st.table(df)


