# modulos/pages/caja_page.py
import streamlit as st
from modulos.db.crud_caja import list_movimientos, create_movimiento

def render_caja():
    st.header("🏦 Caja")
    st.subheader("Movimientos")

    try:
        movs = list_movimientos()
    except Exception as e:
        st.error(f"Error cargando movimientos: {e}")
        movs = []

    st.dataframe(movs, use_container_width=True)

    st.markdown("---")
    with st.expander("➕ Agregar movimiento"):
        with st.form("form_mov", clear_on_submit=True):
            id_ciclo = st.number_input("ID ciclo", min_value=1, value=1)
            tipo = st.selectbox("Tipo", ["ingreso", "egreso"])
            monto = st.number_input("Monto", min_value=0.0, format="%.2f", value=0.0)
            detalle = st.text_input("Detalle")
            submit = st.form_submit_button("Agregar")
            if submit:
                ok = create_movimiento(id_ciclo, tipo, monto, detalle)
                if ok:
                    st.success("Movimiento agregado ✅")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo agregar movimiento.")


