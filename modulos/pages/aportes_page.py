# modulos/pages/aportes_page.py
import streamlit as st
from modulos.db import crud_aporte
from datetime import date

def render_aportes():
    st.title("💰 Aportes / Ahorro")

    # Toggle para mostrar/ocultar el formulario con botón (requeriste botón desplegable)
    if "show_aporte_form" not in st.session_state:
        st.session_state["show_aporte_form"] = False

    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Listado")
    with col2:
        if st.button("➕ Nuevo aporte"):
            st.session_state["show_aporte_form"] = not st.session_state["show_aporte_form"]

    # lista de aportes
    try:
        aportes = crud_aporte.list_aportes(200)
        if not aportes:
            st.info("No hay aportes registrados (o la tabla no existe).")
        else:
            # mostrar como tabla
            st.table(aportes)
    except Exception as e:
        st.error(f"Error cargando aportes: {e}")

    # Formulario (se muestra solo si se activó el toggle)
    if st.session_state["show_aporte_form"]:
        st.markdown("---")
        st.subheader("Registrar aporte")

        with st.form("form_aporte", clear_on_submit=True):
            id_miembro = st.number_input("ID Miembro", min_value=1, value=1)
            id_reunion = st.number_input("ID Reunión (opcional)", min_value=0, value=0)
            monto = st.number_input("Monto", min_value=0.0, format="%.2f", value=0.0)
            fecha = st.date_input("Fecha", value=date.today())
            tipo = st.selectbox("Tipo", ["ahorro", "aporte", "otro"])

            submitted = st.form_submit_button("Guardar aporte")
            if submitted:
                data = {
                    "id_miembro": int(id_miembro),
                    "id_reunion": int(id_reunion) if id_reunion != 0 else None,
                    "monto": float(monto),
                    "fecha": fecha.strftime("%Y-%m-%d"),
                    "tipo": tipo,
                }
                new_id = crud_aporte.create_aporte(data)
                if new_id:
                    st.success(f"Aporte creado correctamente. id = {new_id}")
                else:
                    st.error("Ocurrió un error al crear el aporte.")
                # opcional: refrescar la página para ver la tabla actualizada
                st.experimental_rerun()



