# modulos/pages/ahorro_page.py
import streamlit as st
import pandas as pd

def render_ahorro():
    st.header("💰 Aportes / Ahorro")
    try:
        from modulos.db import crud_ahorro
    except Exception as e:
        st.warning(f"CRUD ahorro no encontrado: {e}")
        st.table([])
        return

    try:
        rows = crud_ahorro.list_ahorros()
        df = pd.DataFrame(rows) if rows else pd.DataFrame([])
    except Exception as e:
        st.error(f"Error cargando ahorros: {e}")
        df = pd.DataFrame([])

    st.table(df)

    st.subheader("Registrar aporte")
    with st.form("form_aporte"):
        id_miembro = st.number_input("ID Miembro", min_value=1, value=1)
        monto = st.number_input("Monto", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Registrar")
        if submitted:
            try:
                ok = crud_ahorro.create_aporte({"id_miembro": id_miembro, "monto": monto})
                if ok:
                    st.success("Aporte registrado.")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo registrar aporte.")
            except Exception as e:
                st.error(f"Error: {e}")

