# modulos/pages/cierre_page.py
import streamlit as st
from modulos.db import crud_cierre

def render_cierre():
    st.header("🔒 Cierres")
    st.write("Crear y ver cierres del sistema")

    # inicializar toggle en session_state (persistente mientras dure la sesión)
    if "show_crear_cierre" not in st.session_state:
        st.session_state["show_crear_cierre"] = False

    # Botón desplegable (toggle)
    if st.button("Crear cierre 🔽"):
        st.session_state["show_crear_cierre"] = not st.session_state["show_crear_cierre"]

    # Mostrar/ocultar el formulario según el toggle
    if st.session_state["show_crear_cierre"]:
        st.markdown("---")
        with st.form("form_crear_cierre"):
            st.info("Si no hay ciclos válidos se creará uno por defecto automáticamente.")
            # sugerir último ciclo (solo para mostrar)
            latest = crud_cierre.get_latest_ciclo()
            id_sugerido = latest["id_ciclo"] if latest else 0

            id_ciclo_input = st.number_input(
                "ID Ciclo (dejar 0 para usar/crear automático)",
                value=int(id_sugerido or 0),
                min_value=0,
                step=1,
            )
            resumen = st.text_area("Resumen del cierre", value="", height=120)
            submitted = st.form_submit_button("Confirmar creación del cierre 🔐")

        if submitted:
            id_to_use = id_ciclo_input if id_ciclo_input > 0 else None
            ok, msg = crud_cierre.create_cierre(id_to_use, resumen)
            if ok:
                st.success(msg)
            else:
                st.error(f"Error al crear cierre: {msg}")

    st.markdown("---")
    st.subheader("Cierres recientes")
    try:
        rows = crud_cierre.list_cierres()
        if rows:
            st.table(rows)
        else:
            st.info("No hay cierres registrados.")
    except Exception as e:
        st.error(f"Error al listar cierres: {e}")

