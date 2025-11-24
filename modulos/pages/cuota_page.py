# modulos/pages/cuota_page.py
import streamlit as st
from modulos.db.crud_cuota import list_cuotas, update_cuota_pay

def render_cuota():
    st.header("📄 Cuotas")
    try:
        filas = list_cuotas()
    except Exception as e:
        st.error(f"Error: {e}")
        filas = []
    st.dataframe(filas, use_container_width=True)

    st.markdown("---")
    st.subheader("Aplicar pago a cuota")
    with st.form("form_aplicar_pago"):
        id_cuota = st.number_input("ID cuota", min_value=1, value=0)
        monto = st.number_input("Monto a abonar", min_value=0.0, format="%.2f")
        if st.form_submit_button("Aplicar pago"):
            if id_cuota and monto>0:
                ok = update_cuota_pay(id_cuota, monto)
                if ok:
                    st.success("Pago aplicado ✅")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo aplicar el pago.")
            else:
                st.error("ID cuota y monto válidos son obligatorios.")
