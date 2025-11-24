# modulos/pages/dashboard_page.py
import streamlit as st

def render_dashboard():
    st.header("📊 Dashboard")
    st.write("Resumen operativo")
    # si tienes funciones de CRUD que retornen métricas, importarlas aquí en try/except
    try:
        from modulos.db import crud_miembros
        total_miembros = crud_miembros.count_miembros() if hasattr(crud_miembros, "count_miembros") else "—"
    except Exception:
        total_miembros = "—"

    c1, c2, c3 = st.columns(3)
    c1.metric("Total miembros", total_miembros)
    c2.metric("Préstamos vigentes", "—")
    c3.metric("Saldo caja", "—")

    st.subheader("Actividad reciente")
    st.table([])  # reemplazar con datos reales cuando existan

