# modulos/pages/dashboard_page.py

import streamlit as st
from modulos.config.conexion import get_engine
import pandas as pd

# ============================================
# DASHBOARD PRINCIPAL
# ============================================

def render_dashboard():
    st.header("📊 Dashboard — Resumen General")

    engine = get_engine()

    try:
        # ===============================
        # Contadores principales
        # ===============================
        query_totales = {
            "Miembros": "SELECT COUNT(*) AS total FROM miembro",
            "Préstamos": "SELECT COUNT(*) AS total FROM prestamo",
            "Ahorros": "SELECT COUNT(*) AS total FROM ahorro",
            "Grupos": "SELECT COUNT(*) AS total FROM grupo",
        }

        col1, col2, col3, col4 = st.columns(4)

        with engine.connect() as conn:
            for label, sql in query_totales.items():
                try:
                    result = conn.execute(sql).scalar()
                except:
                    result = "—"

                if label == "Miembros":
                    col1.metric(label, result)
                elif label == "Préstamos":
                    col2.metric(label, result)
                elif label == "Ahorros":
                    col3.metric(label, result)
                elif label == "Grupos":
                    col4.metric(label, result)

        st.divider()

        # ===============================
        # Últimos movimientos del sistema
        # ===============================
        st.subheader("📌 Actividad reciente (últimos 15 registros)")

        sql_movs = """
        SELECT 
            p.id_prestamo AS id,
            m.nombre AS miembro,
            p.monto AS monto,
            p.estado AS estado
        FROM prestamo p
        LEFT JOIN miembro m ON m.id_miembro = p.id_miembro
        ORDER BY p.id_prestamo DESC
        LIMIT 15;
        """

        try:
            df = pd.read_sql(sql_movs, engine)
            st.dataframe(df)
        except Exception as e:
            st.warning(f"No se pudo cargar la actividad reciente: {e}")

    except Exception as e:
        st.error(f"Error cargando dashboard: {e}")


