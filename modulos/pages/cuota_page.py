# modulos/pages/cuota_page.py
import streamlit as st
import pandas as pd

def render_cuota():
    st.header("📅 Cuotas")
    try:
        from modulos.db import crud_cuota
    except Exception as e:
        st.warning(f"CRUD cuota no encontrado: {e}")
        st.table([])
        return

    try:
        rows = crud_cuota.list_cuotas()
        df = pd.DataFrame(rows) if rows else pd.DataFrame([])
    except Exception as e:
        st.error(f"Error cargando cuotas: {e}")
        df = pd.DataFrame([])

    st.table(df)
