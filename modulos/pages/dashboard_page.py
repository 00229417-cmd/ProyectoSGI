# modulos/pages/dashboard_page.py
import streamlit as st
from sqlalchemy import text
from modulos.config.conexion import get_engine

ICON = "📊"

def render_dashboard():
    st.markdown(f"## {ICON} Dashboard")
    engine = None
    try:
        engine = get_engine()
    except Exception as e:
        st.error(f"No se pudo obtener conexión a la DB: {e}")
        return

    # Helpers con try/except para consultas simples
    def _safe_count(query: str) -> str:
        try:
            with engine.connect() as conn:
                res = conn.execute(text(query)).scalar()
            return str(int(res or 0))
        except Exception as e:
            return f"ERR: {e}"

    total_miembros = _safe_count("SELECT COUNT(*) FROM miembro")
    prestamos_vigentes = _safe_count("SELECT COUNT(*) FROM prestamo WHERE estado IS NULL OR estado NOT IN ('pagado','cerrado','cancelado')")
    saldo_caja = _safe_count("SELECT SUM(saldo_final) FROM caja")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total miembros", total_miembros)
    c2.metric("Préstamos vigentes", prestamos_vigentes)
    c3.metric("Saldo caja (suma)", saldo_caja)

    st.markdown("### Actividad reciente (placeholder)")
    st.info("Aquí puedes agregar widgets/resúmenes. Si faltan tablas/columnas la métricas mostrarán `ERR:` con el mensaje SQL — revisa la estructura de BD.")




