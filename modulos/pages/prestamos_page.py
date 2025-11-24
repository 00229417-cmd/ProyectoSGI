# modulos/pages/prestamos_page.py
import streamlit as st
from sqlalchemy import text
from modulos.config.conexion import get_engine

# intentar importar CRUD ya existente
try:
    from modulos.db.crud_prestamo import list_prestamos, create_prestamo
except Exception:
    list_prestamos = None
    create_prestamo = None

def _fetch_prestamos(limit=200):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("""SELECT id_prestamo, id_promotora, id_ciclo, id_miembro, monto, intereses, saldo_restante, estado
                    FROM prestamo ORDER BY id_prestamo DESC LIMIT :lim""")
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def _insert_prestamo_direct(promotora, ciclo, miembro, monto, intereses, plazo):
    engine = get_engine()
    with engine.begin() as conn:
        q = text("""
            INSERT INTO prestamo (id_promotora, id_ciclo, id_miembro, monto, intereses, saldo_restante, estado, plazo_meses, total_cuotas)
            VALUES (:prom, :cic, :mem, :mto, :int, :saldo, 'vigente', :plazo, 0)
        """)
        res = conn.execute(q, {"prom": promotora, "cic": ciclo, "mem": miembro, "mto": monto, "int": intereses, "saldo": monto, "plazo": plazo})
        try:
            return res.lastrowid or True
        except Exception:
            return True

def prestamos_page():
    st.header("Préstamos")
    st.subheader("Lista de préstamos")

    prestamos = []
    try:
        if list_prestamos:
            prestamos = list_prestamos()
        else:
            prestamos = _fetch_prestamos()
    except Exception as e:
        st.error(f"Error al leer préstamos: {e}")

    if not prestamos:
        st.info("No hay préstamos registrados todavía.")
    else:
        st.table(prestamos)

    st.markdown("---")
    st.subheader("Solicitar nuevo préstamo")

    with st.form("form_prestamo", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            id_promotora = st.number_input("ID promotora", min_value=1, value=1)
            id_ciclo = st.number_input("ID ciclo", min_value=1, value=1)
            id_miembro = st.number_input("ID miembro", min_value=1, value=1)
        with col2:
            monto = st.number_input("Monto", min_value=0.0, format="%.2f", value=100.0)
            intereses = st.number_input("Interés (%)", min_value=0.0, format="%.2f", value=5.0)
            plazo = st.number_input("Plazo (meses)", min_value=1, step=1, value=6)
        submit = st.form_submit_button("Crear préstamo")

        if submit:
            try:
                if create_prestamo:
                    ok = create_prestamo(id_promotora, id_ciclo, id_miembro, monto, intereses, plazo)
                else:
                    ok = _insert_prestamo_direct(id_promotora, id_ciclo, id_miembro, monto, intereses, plazo)
                if ok:
                    st.success("Préstamo registrado correctamente.")
                    try:
                        st.experimental_rerun()
                    except Exception:
                        pass
                else:
                    st.error("No se pudo registrar el préstamo.")
            except Exception as ex:
                st.error(f"Error al crear préstamo: {ex}")


