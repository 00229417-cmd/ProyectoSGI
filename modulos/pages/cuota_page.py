# modulos/pages/cuota_page.py

import streamlit as st
from modulos.db.crud_cuota import obtener_cuotas, crear_cuota

def render_cuota():
    st.header("📅 Gestión de Cuotas")

    # --- Botón para expandir formulario ---
    with st.expander("➕ Crear nueva cuota"):
        with st.form("form_cuota"):
            id_prestamo = st.number_input("ID del préstamo", min_value=1)
            numero_cuota = st.number_input("Número de cuota", min_value=1)
            fecha_vencimiento = st.date_input("Fecha de vencimiento")
            monto_capital = st.number_input("Monto capital", min_value=0.0)
            monto_interes = st.number_input("Monto interés", min_value=0.0)
            monto_total = st.number_input("Monto total", min_value=0.0)
            estado = st.selectbox("Estado", ["pendiente", "pagada", "vencida"])

            enviar = st.form_submit_button("Guardar cuota")

            if enviar:
                data = {
                    "id_prestamo": id_prestamo,
                    "numero_cuota": numero_cuota,
                    "fecha_vencimiento": fecha_vencimiento,
                    "monto_capital": monto_capital,
                    "monto_interes": monto_interes,
                    "monto_total": monto_total,
                    "estado": estado,
                }
                ok = crear_cuota(data)
                if ok:
                    st.success("Cuota creada correctamente")
                else:
                    st.error("Error al crear la cuota")

    # --- Tabla de cuotas ---
    st.subheader("📋 Listado de cuotas")

    try:
        cuotas = obtener_cuotas()
        st.dataframe(cuotas)
    except Exception as e:
        st.error(f"Error cargando cuotas: {e}")

