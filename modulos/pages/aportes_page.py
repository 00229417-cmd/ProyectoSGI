# modulos/pages/aportes_page.py
import streamlit as st
from modulos.db.crud_aporte import list_aportes, create_aporte

def render_aportes():
    st.title("💰 Aportes / Ahorro")

    # ================================
    # LISTADO
    # ================================
    try:
        aportes = list_aportes()
        st.subheader("Listado de aportes")
        st.dataframe(aportes)
    except Exception as e:
        st.error(f"Error cargando aportes: {e}")
        return

    st.divider()

    # ================================
    # FORMULARIO (con botón desplegable)
    # ================================
    with st.expander("➕ Registrar nuevo aporte"):
        id_miembro = st.number_input("ID Miembro", min_value=1, step=1)
        id_reunion = st.number_input("ID Reunión", min_value=1, step=1)
        monto = st.number_input("Monto del aporte", min_value=0.01, step=0.01)
        fecha = st.date_input("Fecha")
        tipo = st.text_input("Tipo de aporte")

        if st.button("Guardar aporte"):
            try:
                nuevo_id = create_aporte(id_miembro, id_reunion, monto, fecha, tipo)
                st.success(f"Aporte registrado correctamente. ID = {nuevo_id}")
                st.rerun()   # <<<< REEMPLAZA experimental_rerun
            except Exception as ex:
                st.error(f"Error guardando aporte: {ex}")




