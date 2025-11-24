# modulos/pages/dashboard_page.py
import streamlit as st
import pandas as pd
from sqlalchemy import text
from modulos.config.conexion import get_engine, test_connection

def render_dashboard():
    st.markdown("### 📊 Dashboard — Resumen operativo")

    ok, msg = test_connection()
    if not ok:
        st.warning(f"DB: NO CONECTADO ({msg})")
        return
    else:
        st.success("DB conectado")

    engine = get_engine()

    # Queries seguras con try/except para no romper la página si faltan tablas/columnas
    def safe_scalar(sql, params=None):
        try:
            with engine.connect() as conn:
                r = conn.execute(text(sql), params or {}).scalar()
                return r
        except Exception:
            return None

    total_miembros = safe_scalar("SELECT COUNT(*) FROM miembro")
    prestamos_vigentes = safe_scalar("SELECT COUNT(*) FROM prestamo WHERE estado IS NULL OR estado <> 'pagado'")
    saldo_caja = safe_scalar("SELECT SUM(saldo_final) FROM caja")

    # Mostrar métricas (si son None -> mostrar guión)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total miembros", str(total_miembros) if total_miembros is not None else "—")
    c2.metric("Préstamos (aprox.)", str(prestamos_vigentes) if prestamos_vigentes is not None else "—")
    c3.metric("Saldo caja (sum)", f"{saldo_caja:.2f}" if isinstance(saldo_caja, (int, float)) else ("—" if saldo_caja is None else str(saldo_caja)))

    st.markdown("---")
    st.subheader("Actividad reciente (últimos registros)")

    # Intentar mostrar últimos aportes / pagos / reportes
    recent_tables = {
        "Aportes (aportes)": "SELECT id_aporte AS id, id_miembro, monto, fecha FROM aporte ORDER BY id_aporte DESC LIMIT 8",
        "Pagos (pago)": "SELECT id_pago AS id, id_prestamo, fecha, monto FROM pago ORDER BY id_pago DESC LIMIT 8",
        "Reportes (reporte)": "SELECT id_reporte AS id, tipo, fecha_generacion AS fecha, descripcion FROM reporte ORDER BY id_reporte DESC LIMIT 8"
    }

    for title, q in recent_tables.items():
        try:
            with engine.connect() as conn:
                df = pd.read_sql_query(text(q), conn)
        except Exception as e:
            st.warning(f"No se pudo cargar {title}: {e}")
            continue

        if not df.empty:
            st.markdown(f"**{title}**")
            st.dataframe(df)
        else:
            st.info(f"No hay registros recientes en {title} (o la tabla no existe).")


