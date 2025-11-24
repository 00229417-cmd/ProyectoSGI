# modulos/pages/ahorro_page.py
import streamlit as st
from modulos.db.crud_ahorro import list_aportes, create_aporte

def render_ahorro():
    st.header("💰 Aportes / Ahorro")
    try:
        rows = list_aportes()
    except Exception as e:
        st.error(f"Error: {e}")
        rows = []
    st.dataframe(rows, use_container_width=True)

    with st.expander("➕ Registrar aporte"):
        with st.form("form_aporte", clear_on_submit=True):
            id_miembro = st.number_input("ID miembro", min_value=1, value=1)
            id_ciclo = st.number_input("ID ciclo", min_value=1, value=1)
            monto = st.number_input("Monto", min_value=0.0, format="%.2f")
            tipo = st.selectbox("Tipo", ["aporte","ahorro_extra","aporte_inicial"])
            desc = st.text_input("Descripción (opcional)")
            if st.form_submit_button("Registrar"):
                ok = create_aporte(id_miembro, id_ciclo, monto, tipo, desc)
                if ok:
                    st.success("Aporte registrado ✅")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo registrar el aporte.")
