# modulos/pages/miembros_page.py
import streamlit as st
import pandas as pd
from modulos.db import crud_miembros

ICON = "👥"

def render_miembros():
    st.markdown(f"## {ICON} Miembros")
    # intento de obtener la lista
    ok, rows, msg = crud_miembros.list_miembros()
    if not ok:
        st.error(f"Error cargando miembros: {msg}")
        # mostramos placeholder vacío pero permitimos crear
        rows = []

    st.subheader("Listado")

    # mostrar tabla (DataFrame) o mensaje si vacío
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay miembros registrados todavía.")

    st.markdown("---")
    # Botón para mostrar/ocultar formulario (persistente en session_state)
    if "show_form_miembro" not in st.session_state:
        st.session_state.show_form_miembro = False

    if st.button("➕ Crear nuevo miembro"):
        st.session_state.show_form_miembro = not st.session_state.show_form_miembro

    if st.session_state.show_form_miembro:
        with st.form("form_nuevo_miembro"):
            st.markdown("### Registrar miembro")
            col1, col2 = st.columns(2)
            nombre = col1.text_input("Nombre")
            apellido = col2.text_input("Apellido")
            dui = st.text_input("DUI / Identificación")
            direccion = st.text_input("Dirección")
            id_tipo_usuario = st.number_input("ID Tipo usuario (opcional)", min_value=0, step=1, value=0)
            submitted = st.form_submit_button("Guardar miembro")
            if submitted:
                # normalizar: si id_tipo_usuario 0 => None
                tip = id_tipo_usuario if id_tipo_usuario and id_tipo_usuario > 0 else None
                okc, new_id, msgc = crud_miembros.create_miembro(nombre=nombre.strip(), apellido=apellido.strip(), dui=dui.strip() or None, direccion=direccion.strip() or None, id_tipo_usuario=tip)
                if okc:
                    st.success(f"Miembro creado correctamente. id = {new_id or '—'}.")
                    # refrescar la página para ver nuevo registro
                    st.experimental_rerun()
                else:
                    st.error(f"No se pudo crear miembro: {msgc}")



