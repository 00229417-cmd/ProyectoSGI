import streamlit as st
from modulos.config.conexion import get_engine
from sqlalchemy import text

def safe_rerun():
    try:
        return st.rerun()
    except Exception:
        try:
            return st.experimental_rerun()
        except:
            st.experimental_set_query_params(_reload="1")

def list_asistencia(limit=500):
    engine = get_engine()
    q = text("""
        SELECT 
            id_asistencia,
            id_miembro,
            id_multa,
            motivo,
            presente_ausente
        FROM asistencia
        ORDER BY id_asistencia DESC
        LIMIT :lim
    """)
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
    return [dict(r) for r in rows]

def create_asistencia(id_miembro, id_multa, motivo, presente_ausente):
    engine = get_engine()
    q = text("""
        INSERT INTO asistencia (
            id_miembro, id_multa, motivo, presente_ausente
        ) VALUES (
            :id_miembro, :id_multa, :motivo, :presente_ausente
        )
    """)
    params = {
        "id_miembro": id_miembro,
        "id_multa": id_multa,
        "motivo": motivo,
        "presente_ausente": presente_ausente
    }
    with engine.begin() as conn:
        conn.execute(q, params)
        last = conn.execute(text("SELECT LAST_INSERT_ID() AS id")).scalar()
    return last

def render_asistencia():
    st.markdown("## ✅ Asistencia")

    if st.button("➕ Registrar asistencia"):
        st.session_state["show_asistencia_form"] = not st.session_state.get("show_asistencia_form", False)

    # Mostrar tabla
    try:
        filas = list_asistencia()
        st.table(filas)
    except Exception as e:
        st.error(f"Error cargando asistencia: {e}")

    # Formulario
    if st.session_state.get("show_asistencia_form", False):
        st.markdown("### Registrar nueva asistencia")
        with st.form("form_asistencia"):
            id_miembro = st.number_input("ID Miembro", min_value=1)
            id_multa = st.number_input("ID Multa (opcional)", min_value=0)
            motivo = st.text_area("Motivo")
            presente_ausente = st.selectbox("Estado", ["presente", "ausente"])

            submitted = st.form_submit_button("Guardar")

        if submitted:
            id_multa_val = id_multa if id_multa > 0 else None
            try:
                new_id = create_asistencia(id_miembro, id_multa_val, motivo, presente_ausente)
                st.success(f"Asistencia registrada. ID: {new_id}")
                safe_rerun()
            except Exception as e:
                st.error(f"Error creando asistencia: {e}")
