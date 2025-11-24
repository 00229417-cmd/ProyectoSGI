# modulos/pages/prestamos_page.py
import streamlit as st
from modulos.db.crud_prestamo import list_prestamos, create_prestamo

def render_prestamos():
    st.header("📄 Préstamos")
    st.subheader("Lista de préstamos")
    try:
        prestamos = list_prestamos()
    except Exception as e:
        st.error(f"Error cargando préstamos: {e}")
        prestamos = []
    st.dataframe(prestamos, use_container_width=True)

    st.markdown("---")
    with st.expander("➕ Solicitar préstamo"):
        with st.form("form_prestamo", clear_on_submit=True):
            id_prom = st.number_input("ID promotora", min_value=1, value=1)
            id_ciclo = st.number_input("ID ciclo", min_value=1, value=1)
            id_miembro = st.number_input("ID miembro", min_value=1, value=1)
            monto = st.number_input("Monto", min_value=0.0, format="%.2f", value=100.0)
            intereses = st.number_input("Interés (%)", min_value=0.0, format="%.2f", value=5.0)
            plazo = st.number_input("Plazo (meses)", min_value=1, value=6)
            submit = st.form_submit_button("Crear préstamo")
            if submit:
                ok = create_prestamo(id_prom, id_ciclo, id_miembro, monto, intereses, plazo)
                if ok:
                    st.success("Préstamo registrado ✅")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo registrar el préstamo.")


