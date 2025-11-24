# modulos/pages/prestamos_page.py
import streamlit as st
from datetime import date, datetime
from modulos.db import crud_prestamo

def render_prestamos():
    st.title("Crear préstamo")

    with st.form("form_crear_prestamo", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            id_ciclo = st.number_input("ID Ciclo", min_value=0, step=1, value=1)
            id_miembro = st.number_input("ID Miembro", min_value=1, step=1, value=1)
            id_promotora = st.number_input("ID Promotora (opcional)", min_value=0, step=1, value=0)
        with col2:
            monto = st.number_input("Monto", min_value=0.0, value=1000.0, format="%.2f")
            intereses = st.number_input("Intereses (%)", min_value=0.0, value=10.0, format="%.2f")
            plazo_meses = st.number_input("Plazo (meses)", min_value=1, step=1, value=6)

        st.markdown("---")
        # Fecha opcional: si el usuario marca la casilla, mostramos date_input
        usar_fecha = st.checkbox("Especificar fecha de solicitud (opcional)", value=False)
        fecha_solicitud_val = None
        if usar_fecha:
            # streamlit en algunas versiones no acepta None como default -> ponemos today
            f_date = st.date_input("Fecha de solicitud", value=date.today())
            # convertir a string 'YYYY-MM-DD' (DB acepta DATETIME/DATE)
            # si además quieres hora, podrías usar datetime.now() o un time input
            fecha_solicitud_val = f_date.isoformat()

        submitted = st.form_submit_button("Crear préstamo")

    if submitted:
        try:
            prom = int(id_promotora) if id_promotora and id_promotora > 0 else None
            prest_id = crud_prestamo.create_prestamo(
                id_ciclo=int(id_ciclo),
                id_miembro=int(id_miembro),
                monto=float(monto),
                intereses=float(intereses),
                plazo_meses=int(plazo_meses),
                id_promotora=prom,
                fecha_solicitud=fecha_solicitud_val
            )
            if prest_id:
                st.success(f"Préstamo creado. id = {prest_id}")
            else:
                st.success("Préstamo creado (id no retornado por el driver). Verifica en la BD.")
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("---")
    st.header("Últimos préstamos")
    try:
        prestamos = crud_prestamo.listar_prestamos(limit=50)
        if prestamos:
            st.dataframe(prestamos)
        else:
            st.info("No se encontraron préstamos.")
    except Exception as e:
        st.error(f"Error cargando préstamos: {e}")



