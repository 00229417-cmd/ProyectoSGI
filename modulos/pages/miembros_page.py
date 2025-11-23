# modulos/pages/miembros_page.py
import streamlit as st
from modulos.db.crud_miembros import listar_miembros, crear_miembro

def mostrar_miembros():
    st.header("Miembros")
    with st.expander("Nuevo miembro"):
        with st.form("form_nuevo_miembro"):
            nombre = st.text_input("Nombre completo")
            identificacion = st.text_input("Identificación")
            telefono = st.text_input("Teléfono")
            direccion = st.text_input("Dirección")
            if st.form_submit_button("Crear miembro"):
                r = crear_miembro(nombre=nombre, identificacion=identificacion, telefono=telefono, direccion=direccion)
                if r:
                    st.success("Miembro creado correctamente.")
                else:
                    st.error("Error al crear miembro.")

    st.subheader("Miembros recientes")
    rows = listar_miembros(limit=100)
    if rows:
        st.table(rows)
    else:
        st.info("No hay miembros registrados.")

