# modulos/pages/prestamos_page.py

import streamlit as st
from modulos.db.crud_prestamo import create_prestamo, listar_prestamos


# =====================================================
# RENDER – PÁGINA DE PRÉSTAMOS
# =====================================================
def render_prestamos():

    st.markdown("## 💸 Préstamos")

    # ================================
    # Mostrar listado
    # ================================
    st.subheader("Listado de préstamos")

    try:
        prestamos = listar_prestamos()
        if prestamos:
            st.table(prestamos)
        else:
            st.info("No hay préstamos registrados aún.")
    except Exception as e:
        st.error(f"Error cargando préstamos: {e}")

    st.write("---")

    # ================================
    # Crear nuevo préstamo
    # ================================
    st.subheader("Crear préstamo")

    # FORMULARIO
    with st.form("form_prestamo"):

        id_ciclo = st.number_input("ID Ciclo", min_value=1)
        id_miembro = st.number_input("ID Miembro", min_value=1)
        id_promotora = st.number_input("ID Promotora (opcional)", min_value=0)

        monto = st.number_input("Monto", min_value=0.0)
        intereses = st.number_input("Intereses (%)", min_value=0.0)
        plazo_meses = st.number_input("Plazo (meses)", min_value=1)

        fecha_solicitud = st.date_input("Fecha de solicitud (opcional)", value=None)

        submitted = st.form_submit_button("Crear préstamo")

    if submitted:
        try:
            fid = create_prestamo(
                id_ciclo=id_ciclo,
                id_miembro=id_miembro,
                monto=monto,
                intereses=intereses,
                plazo_meses=plazo_meses,
                id_promotora=id_promotora or None,
                fecha_solicitud=str(fecha_solicitud) if fecha_solicitud else None
            )

            if fid:
                st.success(f"Préstamo creado correctamente. ID: {fid}")
                st.rerun()
            else:
                st.error("No se pudo obtener el ID del préstamo creado.")

        except Exception as e:
            st.error(f"Error creando préstamo: {e}")



