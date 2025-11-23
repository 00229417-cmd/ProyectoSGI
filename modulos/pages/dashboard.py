# modulos/pages/dashboard.py
import streamlit as st
from modulos.db.crud_reporte import reporte_resumen_operativo
from modulos.db.crud_caja import obtener_saldo_actual, listar_movimientos

def render_dashboard():
    st.header("Dashboard — Resumen operativo (Premium)")
    rpt = reporte_resumen_operativo()
    saldo = obtener_saldo_actual()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Miembros", rpt.get("total_miembros", 0))
    with c2:
        st.metric("Préstamos vigentes", rpt.get("prestamos_vigentes", 0))
    with c3:
        st.metric("Saldo caja", f"${saldo:,.2f}")
    st.markdown("---")
    st.subheader("Movimientos recientes")
    movs = listar_movimientos(limit=8)
    if movs:
        st.table(movs)
    else:
        st.info("No hay movimientos registrados.")

