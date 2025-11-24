# modulos/pages/aportes_page.py
import streamlit as st
from datetime import date
from modulos.db.crud_aporte import list_aportes, create_aporte

def render_aportes():
    st.title("💰 Aportes")

    # Mostrar listado
    try:
        aportes = list_aportes()
        st.subheader("Listado de aportes")
        if aportes:
            st.dataframe(aportes)
        else:
            st.info("No hay aportes registrados.")
    except Exception as e:
        st.error(f"Error cargando aportes: {e}")
        return

    st.divider()

    # Formulario dentro de un expander (botón desplegable)
    with st.expander("➕ Registrar nuevo aporte"):
        col1, col2 = st.columns([2,1])
        with col1:
            id_miembro = st.number_input("ID Miembro", min_value=1, step=1, value=1)
            id_reunion = st.number_input("ID Reunión (opcional)", min_value=0, step=1, value=0)
            # si prefieres permitir NULL en id_reunion: pasar 0 -> None
        with col2:
            tipo = st.selectbox("Tipo", ["aporte", "ahorro", "otro"])
            monto = st.number_input("Monto", min_value=0.0, step=0.01, format="%.2f")
            fecha = st.date_input("Fecha", value=date.today())

        if st.button("Guardar aporte"):
            # normalizar id_reunion
            id_reunion_val = None if id_reunion == 0 else int(id_reunion)
            try:
                nuevo_id = create_aporte(
                    int(id_miembro),
                    id_reunion_val,
                    float(monto),
                    fecha,
                    tipo
                )
                st.success(f"Aporte registrado correctamente. ID = {nuevo_id}")
                # rerun para refrescar listado
                st.rerun()
            except Exception as ex:
                st.error(f"Error guardando aporte: {ex}")




