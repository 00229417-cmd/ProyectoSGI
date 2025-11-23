# modulos/pages/caja_page.py
import streamlit as st
from modulos.db.crud_caja import registrar_movimiento, listar_movimientos, obtener_saldo_actual

def mostrar_caja():
    st.header("Caja")
    with st.expander("Registrar movimiento"):
        with st.form("form_caja"):
            tipo = st.selectbox("Tipo", ["ingreso", "egreso"])
            monto = st.number_input("Monto", min_value=0.0, format="%.2f")
            detalle = st.text_area("Detalle")
            if st.form_submit_button("Registrar"):
                ok = registrar_movimiento(tipo, monto, detalle)
                if ok:
                    st.success("Movimiento registrado.")
                else:
                    st.error("Error al registrar movimiento.")
    st.subheader("Saldo actual")
    saldo = obtener_saldo_actual()
    st.metric("Saldo caja", f"${saldo:,.2f}")
    st.subheader("Movimientos recientes")
    rows = listar_movimientos(limit=50)
    if rows:
        st.table(rows)

