# modulos/pages/dashboard_page.py
import streamlit as st
import pandas as pd
from sqlalchemy import text
from modulos.config.conexion import get_engine, test_connection

def _safe_scalar(engine, sql, params=None):
    """Ejecuta una consulta que devuelve un solo valor y devuelve None si falla."""
    try:
        with engine.connect() as conn:
            r = conn.execute(text(sql), params or {})
            # scalar() puede lanzar si la columna no existe; capturamos antes
            val = r.scalar()
            return val
    except Exception:
        return None

def _safe_df(engine, sql, params=None):
    """Devuelve un DataFrame o None si falla (tabla/columna ausente)."""
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(text(sql), conn, params=params or {})
            return df
    except Exception:
        return None

def _fmt_number(val):
    """Formatea números seguros para mostrar en metric."""
    try:
        if val is None:
            return "—"
        if isinstance(val, (int, float)):
            return f"{val:,}" if isinstance(val, int) else f"{val:,.2f}"
        # intentar convertir a float
        v = float(val)
        return f"{v:,.2f}"
    except Exception:
        return str(val)

def render_dashboard():
    st.markdown("### 📊 Dashboard — Resumen operativo")


    
    engine = None
    try:
        engine = get_engine()
    except Exception as e:
        st.error(f"Error inicializando engine: {e}")

    # METRICAS PRINCIPALES (usamos safe calls)
    total_miembros = None
    prestamos_vigentes = None
    saldo_caja = None

    if engine:
        total_miembros = _safe_scalar(engine, "SELECT COUNT(*) FROM miembro")
        prestamos_vigentes = _safe_scalar(engine, "SELECT COUNT(*) FROM prestamo WHERE estado IS NULL OR estado <> 'pagado'")
        # saldo caja puede no existir o la columna saldo_final puede no existir
        saldo_caja = _safe_scalar(engine, "SELECT SUM(saldo_final) FROM caja")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total miembros", _fmt_number(total_miembros))
    c2.metric("Préstamos (aprox.)", _fmt_number(prestamos_vigentes))
    # Mostrar saldo con símbolo si es numérico
    if isinstance(saldo_caja, (int, float)):
        c3.metric("Saldo caja (sum)", f"{saldo_caja:,.2f}")
    else:
        c3.metric("Saldo caja (sum)", _fmt_number(saldo_caja))

    st.markdown("---")
    st.subheader("Actividad reciente (últimos registros)")

    recent_tables = {
        "Aportes": "SELECT id_aporte AS id, id_miembro, monto, fecha FROM aporte ORDER BY id_aporte DESC LIMIT 8",
        "Pagos": "SELECT id_pago AS id, id_prestamo, fecha, monto FROM pago ORDER BY id_pago DESC LIMIT 8",
        "Reportes": "SELECT id_reporte AS id, tipo, fecha_generacion AS fecha, descripcion FROM reporte ORDER BY id_reporte DESC LIMIT 8"
    }

    any_shown = False
    for title, q in recent_tables.items():
        if not engine:
            st.info(f"{title}: base de datos no disponible.")
            continue

        df = _safe_df(engine, q)
        if df is None:
            st.warning(f"No se pudo cargar {title} (tabla o columnas faltantes).")
            continue

        if df.empty:
            st.info(f"No hay registros recientes en {title}.")
            continue

        any_shown = True
        st.markdown(f"**{title}**")
        # Mostrar un máximo de filas con ancho
        st.dataframe(df, use_container_width=True)

    if not any_shown:
        st.info("No se pudieron recuperar registros recientes (tablas `aporte`, `pago` o `reporte` faltantes o vacías).")

    # Sección de acciones rápidas (no rompe si faltan endpoints)
    st.markdown("---")
    st.subheader("Acciones rápidas")
    cols = st.columns([1,1,2])
    with cols[0]:
        if st.button("Ver Miembros"):
            try:
                # import dinámico para no obligar a existir
                from modulos.db.crud_miembros import obtener_miembros
                rows = obtener_miembros(limit=10)
                st.dataframe(rows)
            except Exception as e:
                st.error(f"No se pudo mostrar miembros: {e}")
    with cols[1]:
        if st.button("Ver Préstamos"):
            try:
                from modulos.db.crud_prestamo import listar_prestamos
                rows = listar_prestamos() or []
                st.dataframe(rows[:10])
            except Exception as e:
                st.error(f"No se pudo mostrar préstamos: {e}")
    with cols[2]:
        if st.button("Refrescar dashboard"):
            try:
                if hasattr(st, "rerun"):
                    st.rerun()
                else:
                    st.experimental_set_query_params(_reload="1")
            except Exception:
                st.info("Recarga manual (F5) si no hay API de rerun disponible.")

# Alias para compatibilidad con el importador dinámico
def dashboard_page():
    render_dashboard()



