# modulos/pages/dashboard_page.py
import streamlit as st
from modulos.db.crud_miembros import list_miembros
from modulos.db.crud_prestamo import list_prestamos
from modulos.db.crud_caja import list_movimientos

def render_dashboard():
    st.header("📊 Dashboard")
    c1, c2, c3 = st.columns(3)
    try:
        miembros = list_miembros(1)
        total_miembros = len(list_miembros(500))
    except Exception:
        total_miembros = "—"

    try:
        prestamos = list_prestamos(500)
        prestamos_vigentes = len([p for p in prestamos if p.get("estado")=="vigente"]) if prestamos else "—"
    except Exception:
        prestamos_vigentes = "—"

    try:
        movimientos = list_movimientos(10)
        saldo = sum([(m.get("ingresos") or 0) - (m.get("egresos") or 0) for m in movimientos]) if movimientos else "—"
    except Exception:
        saldo = "—"

    c1.metric("Miembros", total_miembros, "👤")
    c2.metric("Préstamos vigentes", prestamos_vigentes, "📄💸")
    c3.metric("Saldo caja", f"${saldo}" if isinstance(saldo,(int,float)) else saldo, "🏦")

    st.subheader("Actividad reciente")
    try:
        st.table(movimientos or [])
    except Exception:
        st.write("No hay actividad reciente.")


