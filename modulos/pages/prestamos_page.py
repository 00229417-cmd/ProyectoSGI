# modulos/pages/prestamos_page.py
import streamlit as st
from modulos.db.crud_prestamo import listar_prestamos, solicitar_prestamo

def mostrar_prestamos():
    st.header("Préstamos")
    with st.expander("Solicitar préstamo"):
        with st.form("form_prestamo"):
            id_miembro = st.number_input("ID miembro", min_value=1, step=1)
            monto = st.number_input("Monto", min_value=0.0, format="%.2f")
            plazo = st.number_input("Plazo (meses)", min_value=1, step=1)
            tasa = st.number_input("Tasa interés (%)", min_value=0.0, format="%.2f")
            if st.form_submit_button("Solicitar"):
                ok = solicitar_prestamo(id_miembro, monto, plazo, tasa)
                if ok:
                    st.success("Solicitud registrada.")
                else:
                    st.error("Error al registrar préstamo.")

    st.subheader("Préstamos recientes")
    rows = listar_prestamos(limit=100)
    if rows:
        st.table(rows)

