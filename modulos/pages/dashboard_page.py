# modulos/pages/dashboard_page.py
import streamlit as st
from sqlalchemy import text
from modulos.config.conexion import get_engine

ICON = "📊"

def render_dashboard():
    st.markdown(f"## {ICON} Dashboard")
    engine = get_engine()

    # métricas simples: total miembros, prestamos vigentes, saldo caja
    try:
        with engine.connect() as conn:
            total_miembros = conn.execute(text("SELECT COUNT(*) AS c FROM miembro")).fetchone()._mapping["c"]
            prestamos_vigentes = conn.execute(text("SELECT COUNT(*) AS c FROM prestamo WHERE estado IS NULL OR estado <> 'finalizado'")).fetchone()._mapping["c"]
            saldo_caja_row = conn.execute(text("SELECT SUM(saldo_final) AS s FROM caja")).fetchone()._mapping
            saldo_caja = saldo_caja_row.get("s") if saldo_caja_row else None

            # actividad reciente: últimos aportes (si existe la tabla aporte)
            try:
                recent = conn.execute(text(
                    "SELECT id_aporte, id_miembro, monto, fecha, tipo FROM aporte ORDER BY id_aporte DESC LIMIT 6"
                )).fetchall()
                recent_list = [dict(r._mapping) for r in recent]
            except Exception:
                recent_list = []
    except Exception as e:
        st.error(f"Error leyendo métricas: {e}")
        st.stop()
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Total miembros", str(total_miembros))
    c2.metric("Préstamos vigentes", str(prestamos_vigentes))
    c3.metric("Saldo caja", f"{saldo_caja if saldo_caja is not None else '—'}")

    st.markdown("### Actividad reciente (últimos aportes)")
    if recent_list:
        st.table(recent_list)
    else:
        st.info("No hay actividad reciente para mostrar.")



