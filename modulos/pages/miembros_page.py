# modulos/pages/miembros_page.py
import streamlit as st
from modulos.db.crud_miembros import list_miembros, create_miembro, get_miembro_by_id, update_miembro, delete_miembro

def render_miembros():
    st.header("👥 Miembros")
    st.subheader("Lista de miembros")

    try:
        miembros = list_miembros()
    except Exception as e:
        st.error(f"Error cargando miembros: {e}")
        miembros = []

    st.dataframe(miembros, use_container_width=True)

    st.markdown("---")
    with st.expander("➕ Crear nuevo miembro"):
        with st.form("form_nuevo_miembro", clear_on_submit=True):
            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
            dui = st.text_input("DUI")
            direccion = st.text_area("Dirección")
            tipo = st.number_input("ID tipo usuario", min_value=1, value=2)
            submit = st.form_submit_button("Guardar")
            if submit:
                ok = create_miembro(nombre=nombre, apellido=apellido, id_tipo_usuario=tipo, dui=dui, direccion=direccion)
                if ok:
                    st.success("Miembro creado ✅")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo crear el miembro.")



