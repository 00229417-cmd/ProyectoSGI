# modulos/pages/miembros_page.py
import streamlit as st
import pandas as pd

def render_miembros():
    st.header("👥 Miembros")
    try:
        from modulos.db import crud_miembros
    except Exception as e:
        st.warning(f"CRUD de miembros no encontrado: {e}")
        st.info("Crea modulos/db/crud_miembros.py con funciones: list_miembros(), create_miembro(data), update_miembro(id, data), delete_miembro(id)")
        st.table([])
        return

    # LISTADO
    try:
        rows = crud_miembros.list_miembros(limit=500)
        df = pd.DataFrame(rows) if rows is not None else pd.DataFrame([])
    except Exception as e:
        st.error(f"Error cargando miembros: {e}")
        df = pd.DataFrame([])

    st.subheader("Listado")
    st.table(df)

    st.subheader("Crear nuevo miembro")
    with st.form("form_create_miembro"):
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        dui = st.text_input("DUI")
        direccion = st.text_input("Dirección")
        submitted = st.form_submit_button("Crear")
        if submitted:
            try:
                datos = {"nombre": nombre, "apellido": apellido, "dui": dui, "direccion": direccion}
                ok = crud_miembros.create_miembro(datos)
                if ok:
                    st.success("Miembro creado.")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo crear el miembro.")
            except Exception as e:
                st.error(f"Error al crear miembro: {e}")



