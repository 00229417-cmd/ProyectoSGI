# modulos/pages/miembros_page.py
import streamlit as st
from modulos.db.crud_miembros import list_miembros, create_miembro

ICON = "👥"

def render_miembros():
    st.markdown(f"## {ICON} Miembros")
    # Mensaje de carga
    try:
        miembros = list_miembros(500)
    except Exception as e:
        st.error(f"Error cargando miembros: {e}")
        miembros = []

    st.subheader("Listado")
    if miembros:
        # mostrar tabla con st.dataframe para copiar/pegar
        st.dataframe(miembros, use_container_width=True)
    else:
        st.info("No hay miembros registrados todavía.")

    st.markdown("---")

    # Botón para mostrar/ocultar formulario de creación
    if "show_new_miembro" not in st.session_state:
        st.session_state["show_new_miembro"] = False

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("➕ Crear nuevo miembro"):
            st.session_state["show_new_miembro"] = not st.session_state["show_new_miembro"]

    with col2:
        st.write("")  # espacio

    if st.session_state["show_new_miembro"]:
        st.markdown("### Crear nuevo miembro")
        with st.form("form_crear_miembro", clear_on_submit=False):
            id_tipo_usuario = st.number_input("ID tipo usuario (opcional)", min_value=0, value=0, step=1)
            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
            dui = st.text_input("DUI")
            direccion = st.text_input("Dirección")
            submitted = st.form_submit_button("Guardar miembro")
            if submitted:
                # normalizar valor opcional
                id_tipo_val = id_tipo_usuario if id_tipo_usuario and id_tipo_usuario > 0 else None
                ok, msg = create_miembro(id_tipo_val, nombre.strip(), apellido.strip(), dui.strip(), direccion.strip())
                if ok:
                    st.success(msg)
                    st.session_state["show_new_miembro"] = False
                    # recargar para ver el miembro en la tabla
                    try:
                        st.experimental_rerun()
                    except Exception:
                        st.info("Recarga manual necesaria para ver cambios.")
                else:
                    st.error(msg)



