# modulos/pages/reunion_page.py
import streamlit as st
from modulos.config.conexion import get_engine
from sqlalchemy import text

def _ensure_state_keys():
    st.session_state.setdefault("show_form_reunion", False)
    st.session_state.setdefault("last_reunion_created", None)

def _listar_reuniones(limit=200):
    engine = get_engine()
    q = text("""
        SELECT
            id_reunion,
            id_grupo,
            id_asistencia,
            fecha,
            dia,
            lugar,
            extraordinaria_ordinaria
        FROM reunion
        ORDER BY id_reunion DESC
        LIMIT :lim
    """)
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def _crear_reunion(id_grupo, id_asistencia, fecha, dia, lugar, tipo_reunion):
    engine = get_engine()
    q = text("""
        INSERT INTO reunion (
            id_grupo, id_asistencia, fecha, dia, lugar, extraordinaria_ordinaria
        ) VALUES (
            :id_grupo, :id_asistencia, :fecha, :dia, :lugar, :tipo_reunion
        )
    """)
    params = {
        "id_grupo": id_grupo,
        "id_asistencia": id_asistencia,
        "fecha": fecha,
        "dia": dia,
        "lugar": lugar,
        "tipo_reunion": tipo_reunion,
    }
    with engine.begin() as conn:
        conn.execute(q, params)
        last = conn.execute(text("SELECT LAST_INSERT_ID() AS id")).scalar()
        try:
            return int(last)
        except Exception:
            return None

def render_reunion():
    _ensure_state_keys()
    st.markdown("## 🗓️ Reuniones")

    cols = st.columns([1, 5])
    with cols[0]:
        if st.button("➕ Nueva reunión"):
            st.session_state["show_form_reunion"] = not st.session_state["show_form_reunion"]
    with cols[1]:
        st.write("")

    st.subheader("Listado de reuniones")
    try:
        reuniones = _listar_reuniones()
        if not reuniones:
            st.info("No hay reuniones registradas.")
        else:
            st.table(reuniones)
    except Exception as e:
        st.error(f"Error cargando reuniones: {e}")

    st.markdown("---")

    if st.session_state["show_form_reunion"]:
        st.subheader("Crear nueva reunión")
        with st.form("form_reunion"):
            id_grupo = st.number_input("ID Grupo", min_value=1, value=1)
            id_asistencia = st.number_input("ID Asistencia (opcional)", min_value=0, value=0)
            fecha = st.date_input("Fecha")
            dia = st.text_input("Día (ej. Lunes)")
            lugar = st.text_input("Lugar")
            tipo = st.selectbox("Tipo", ["ordinaria", "extraordinaria"])
            submitted = st.form_submit_button("Guardar reunión")

        if submitted:
            try:
                id_asistencia_val = int(id_asistencia) if id_asistencia and int(id_asistencia) > 0 else None
                new_id = _crear_reunion(
                    id_grupo=int(id_grupo),
                    id_asistencia=id_asistencia_val,
                    fecha=str(fecha),
                    dia=dia,
                    lugar=lugar,
                    tipo_reunion=tipo
                )
                if new_id:
                    st.success(f"Reunión creada. ID: {new_id}")
                    st.session_state["last_reunion_created"] = new_id
                    st.experimental_rerun()
                else:
                    st.error("No se pudo crear la reunión.")
            except Exception as e:
                st.error(f"Error al crear reunión: {e}")


