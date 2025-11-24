# modulos/pages/prestamos_page.py
import streamlit as st
import pandas as pd

def render_prestamos():
    st.header("🏦 Préstamos")
    try:
        from modulos.db import crud_prestamo
    except Exception as e:
        st.warning(f"CRUD prestamo no encontrado: {e}")
        st.table([])
        return

    try:
        rows = crud_prestamo.list_prestamos()
        df = pd.DataFrame(rows) if rows else pd.DataFrame([])
    except Exception as e:
        st.error(f"Error cargando préstamos: {e}")
        df = pd.DataFrame([])

    st.table(df)

    st.subheader("Crear préstamo")
    with st.form("form_prestamo"):
        id_miembro = st.number_input("ID Miembro", min_value=1, value=1)
        monto = st.number_input("Monto", min_value=0.0, format="%.2f")
        plazo = st.number_input("Plazo (meses)", min_value=1, value=6)
        submitted = st.form_submit_button("Crear préstamo")
        if submitted:
            try:
                ok = crud_prestamo.create_prestamo({"id_miembro": id_miembro, "monto": monto, "plazo_meses": plazo})
                if ok:
                    st.success("Préstamo creado.")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo crear el préstamo.")
            except Exception as e:
                st.error(f"Error: {e}")



