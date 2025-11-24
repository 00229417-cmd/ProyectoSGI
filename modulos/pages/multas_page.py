import streamlit as st
from modulos.config.conexion import get_engine
from sqlalchemy import text

def safe_rerun():
    try:
        st.rerun()
    except:
        try:
            st.experimental_rerun()
        except:
            st.experimental_set_query_params(_reload="1")

def list_multas(limit=200):
    engine = get_engine()
    q = text("""
        SELECT
            id_multa,
            id_miembro,
            tipo,
            monto,
            descripcion,
            fecha,
            estado
        FROM multa
        ORDER BY id_multa DESC
        LIMIT :lim
    """)
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
    return [dict(r) for r in rows]

def create_multa(id_miembro, tipo, monto, descripcion, fecha, estado):
    engine = get_engine()
    q = text("""
        INSERT INTO multa (
            id_miembro, tipo, monto, descripcion, fecha, estado
        ) VALUES (
            :id_miembro, :tipo, :monto, :descripcion, :fecha, :estado
        )
    """)
    params = {
        "id_miembro": id_miembro,
        "tipo": tipo,
        "monto": monto,
        "descripcion": descripcion,
        "fecha": fecha,
        "estado": estado
    }
    with engine.begin() as conn:
        conn.execute(q, params)
        last = conn.execute(text("SELECT LAST_INSERT_ID() AS id")).scalar()
    return last

def render_multas():
    st.markdown("## ⚖️ Multas")

    if st.button("➕ Registrar multa"):
        st.session_state["show_form_multa"] = not st.session_state.get("show_form_multa", False)

    # Mostrar multas
    try:
        filas = list_multas()
        st.table(filas)
    except Exception as e:
        st.error(f"Error cargando multas: {e}")

    if st.session_state.get("show_form_multa", False):
        st.markdown("### Registrar nueva multa")
        with st.form("form_multa"):
            id_miembro = st.number_input("ID Miembro", min_value=1)
            tipo = st.text_input("Tipo de multa")
            monto = st.number_input("Monto", min_value=0.00, format="%.2f")
            descripcion = st.text_area("Descripción")
            fecha = st.date_input("Fecha")
            estado = st.selectbox("Estado", ["pendiente", "pagada"])

            submitted = st.form_submit_button("Guardar multa")

        if submitted:
            try:
                new_id = create_multa(id_miembro, tipo, monto, descripcion, str(fecha), estado)
                st.success(f"Multa registrada. ID: {new_id}")
                safe_rerun()
            except Exception as e:
                st.error(f"Error guardando multa: {e}")

