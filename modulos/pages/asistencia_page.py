# modulos/pages/asistencia_page.py
import streamlit as st
from sqlalchemy import text
from modulos.config.conexion import get_engine


# ================================
# RERUN seguro (sin experimental_rerun)
# ================================
def safe_rerun():
    try:
        st.rerun()
    except:
        try:
            st.experimental_set_query_params(_reload="1")
        except:
            st.info("Recarga la página manualmente (F5).")


# ================================
# CONSULTAR ASISTENCIAS
# ================================
def list_asistencia(limit=500):
    engine = get_engine()
    q = text("""
        SELECT 
            id_asistencia,
            id_miembro,
            id_reunion,
            id_multa,
            motivo,
            presente_ausente,
            fecha
        FROM asistencia
        ORDER BY id_asistencia DESC
        LIMIT :lim
    """)
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
    return [dict(r) for r in rows]


# ================================
# CREAR ASISTENCIA
# ================================
def create_asistencia(id_miembro, id_reunion, id_multa, motivo, estado):
    engine = get_engine()
    q = text("""
        INSERT INTO asistencia (
            id_miembro, id_reunion, id_multa, motivo, presente_ausente, fecha
        ) VALUES (
            :id_miembro, :id_reunion, :id_multa, :motivo, :estado, NOW()
        )
    """)

    params = {
        "id_miembro": id_miembro,
        "id_reunion": id_reunion,
        "id_multa": id_multa,
        "motivo": motivo,
        "estado": estado
    }

    with engine.begin() as conn:
        conn.execute(q, params)
        last = conn.execute(text("SELECT LAST_INSERT_ID() AS id")).scalar()

    return last


# ================================
# PÁGINA PRINCIPAL
# ================================
def render_asistencia():
    st.header("✅ Registro de Asistencia")

    # toggle persistente
    if "show_asistencia_form" not in st.session_state:
        st.session_state["show_asistencia_form"] = False

    # Botón desplegable
    if st.button("Registrar asistencia 🔽"):
        st.session_state["show_asistencia_form"] = not st.session_state["show_asistencia_form"]

    # mostrar tabla
    try:
        filas = list_asistencia()
        st.table(filas)
    except Exception as e:
        st.error(f"Error cargando asistencia: {e}")

    # FORMULARIO (solo si toggle activo)
    if st.session_state["show_asistencia_form"]:
        st.markdown("### Nueva asistencia")
        with st.form("form_asistencia"):

            id_miembro = st.number_input("ID Miembro", min_value=1)
            id_reunion = st.number_input("ID Reunión", min_value=0)
            id_multa = st.number_input("ID Multa (opcional)", min_value=0)

            motivo = st.text_area("Motivo (opcional)")
            estado = st.selectbox("Estado", ["presente", "ausente"])

            submit = st.form_submit_button("Guardar asistencia")

        if submit:
            try:
                new_id = create_asistencia(
                    id_miembro=id_miembro,
                    id_reunion=id_reunion if id_reunion > 0 else None,
                    id_multa=id_multa if id_multa > 0 else None,
                    motivo=motivo,
                    estado=estado
                )
                st.success(f"Asistencia registrada. ID: {new_id}")
                safe_rerun()
            except Exception as e:
                st.error(f"Error registrando asistencia: {e}")

