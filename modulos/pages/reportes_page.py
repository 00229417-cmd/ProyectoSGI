# modulos/pages/reportes_page.py
import streamlit as st
from modulos.db.crud_reporte import reporte_resumen_operativo

def mostrar_reportes():
    st.header("Reportes")
    rpt = reporte_resumen_operativo()
    st.metric("Total miembros", rpt.get("total_miembros", 0))
    st.metric("Préstamos vigentes", rpt.get("prestamos_vigentes", 0))
    st.info("Puedes generar PDF/Excel desde services/report_service.py (pendiente de implementar).")

