# modulos/pages/prestamos_page.py
import streamlit as st
from modulos.db.crud_prestamo import listar_prestamos, create_prestamo

def _ensure_state_keys():
    st.session_state.setdefault("show_form_prestamo", False)
    st.session_state.setdefault("prestamo_last_created", None)

def render_prestamos():
    _ensure_state_keys()

    st.markdown("## 💸 Préstamos")

    # BOTÓN DESPLEGABLE (el usuario pidió explícito que sea botón)
    cols = st.columns([1, 5])
    with cols[0]:
        if st.button("➕ Nuevo préstamo"):
            # alterna visibilidad del formulario
            st.session_state["show_form_prestamo"] = not st.session_state["show_form_prestamo"]

    with cols[1]:
        st.write("")  # espacio para mantener diseño alineado

    # =========== LISTADO ===========
    st.subheader("Listado de préstamos")
    try:
        prestamos = listar_prestamos()
        # Aseguramos que sea lista
        if not prestamos:
            st.info("No hay préstamos registrados.")
        else:
            # mostramos como tabla (lista de dicts)
            st.table(prestamos)
    except Exception as e:
        st.error(f"Error cargando préstamos: {e}")

    st.markdown("---")

    # =========== FORMULARIO (desplegable por botón) ===========
    if st.session_state["show_form_prestamo"]:
        st.subheader("Crear nuevo préstamo")

        with st.form("form_prestamo"):
            id_ciclo = st.number_input("ID Ciclo", min_value=1, value=1)
            id_miembro = st.number_input("ID Miembro", min_value=1, value=1)
            id_promotora = st.number_input("ID Promotora (opcional, 0 si ninguno)", min_value=0, value=0)
            monto = st.number_input("Monto", min_value=0.0, format="%.2f", value=0.0)
            intereses = st.number_input("Intereses (%)", min_value=0.0, format="%.2f", value=0.0)
            plazo_meses = st.number_input("Plazo (meses)", min_value=1, value=1)
            fecha_solicitud = st.date_input("Fecha de solicitud")

            submitted = st.form_submit_button("Guardar préstamo")

        if submitted:
            try:
                fid = create_prestamo(
                    id_ciclo=int(id_ciclo),
                    id_miembro=int(id_miembro),
                    monto=float(monto),
                    intereses=float(intereses),
                    plazo_meses=int(plazo_meses),
                    id_promotora=(int(id_promotora) if id_promotora and int(id_promotora) > 0 else None),
                    fecha_solicitud=str(fecha_solicitud) if fecha_solicitud else None
                )
                if fid:
                    st.success(f"Préstamo creado. ID: {fid}")
                    st.session_state["prestamo_last_created"] = fid
                    # refrescar la página para que se vea el nuevo registro
                    st.experimental_rerun()
                else:
                    st.error("No se pudo obtener ID del préstamo creado.")
            except Exception as e:
                st.error(f"Error guardando préstamo: {e}")


