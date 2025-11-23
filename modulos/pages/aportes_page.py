# modulos/pages/aportes_page.py
import streamlit as st
from modulos.db.crud_aporte import listar_aportes, registrar_aporte

def mostrar_aportes():
    st.header("Aportes")
    with st.expander("Registrar aporte"):
        with st.form("form_aporte"):
            id_miembro = st.number_input("ID miembro", min_value=1, step=1)
            monto = st.number_input("Monto", min_value=0.0, format="%.2f")
            if st.form_submit_button("Registrar aporte"):
                ok = registrar_aporte(id_miembro, monto)
                if ok:
                    st.success("Aporte registrado.")
                else:
                    st.error("Error al registrar aporte.")
    st.subheader("Aportes recientes")
    rows = listar_aportes(limit=100)
    if rows:
        st.table(rows)
    else:
        st.info("No hay aportes.")


