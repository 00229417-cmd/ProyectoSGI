# modulos/pages/cierre_page.py
import streamlit as st
from modulos.db import crud_cierre

def render_cierre():
    st.header("Cierres")
    st.write("Crear y ver cierres del sistema")

    # Obtener último ciclo (si hay) para mostrar por defecto
    latest = crud_cierre.get_latest_ciclo()
    opciones = []
    if latest:
        opciones.append((latest["id_ciclo"], f"Último: {latest['id_ciclo']} ({latest['estado']})"))
    # también permitir que el usuario escriba manualmente el id de ciclo
    st.info("Si no existe ciclo válido se creará uno por defecto automáticamente.")

    with st.form("form_crear_cierre"):
        # mostrar id sugerido pero permitir entrada manual
        id_sugerido = latest["id_ciclo"] if latest else None
        id_ciclo_input = st.number_input("ID Ciclo (dejar 0 para usar/crear automático)", value=int(id_sugerido or 0), min_value=0, step=1)
        resumen = st.text_area("Resumen del cierre", value="")
        submitted = st.form_submit_button("Crear cierre 🔒")

    if submitted:
        id_to_use = id_ciclo_input if id_ciclo_input > 0 else None
        ok, msg = crud_cierre.create_cierre(id_to_use, resumen)
        if ok:
            st.success(msg)
        else:
            st.error(f"Error al crear cierre: {msg}")

    st.divider()
    st.subheader("Cierres recientes")
    try:
        rows = crud_cierre.list_cierres()
        if rows:
            st.table(rows)
        else:
            st.info("No hay cierres registrados.")
    except Exception as e:
        st.error(f"Error al listar cierres: {e}")

