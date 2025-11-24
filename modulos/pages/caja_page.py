# modulos/pages/caja_page.py
import streamlit as st
from sqlalchemy import text
from modulos.config.conexion import get_engine

try:
    from modulos.db.crud_caja import list_movimientos, create_movimiento
except Exception:
    list_movimientos = None
    create_movimiento = None

def _fetch_movimientos(limit=200):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("""SELECT id_caja, id_ciclo, id_ahorro, id_prestamo, id_pago, saldo_inicial, ingresos, egresos, saldo_final
                    FROM caja ORDER BY id_caja DESC LIMIT :lim""")
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def _insert_mov_direct(id_ciclo, tipo, monto, detalle):
    engine = get_engine()
    with engine.begin() as conn:
        # este insert es ejemplo flexible: adapta a tu estructura real de 'caja' si es diferente
        q = text("""
            INSERT INTO caja (id_ciclo, ingresos, egresos, saldo_inicial, saldo_final)
            VALUES (:ciclo, :ing, :eg, 0, :saldo_final)
        """)
        ing = monto if tipo == "ingreso" else 0
        eg = monto if tipo == "egreso" else 0
        saldo_final = ing - eg
        res = conn.execute(q, {"ciclo": id_ciclo, "ing": ing, "eg": eg, "saldo_final": saldo_final})
        try:
            return res.lastrowid or True
        except Exception:
            return True

def caja_page():
    st.header("Caja")
    st.subheader("Movimientos de caja")

    movimientos = []
    try:
        if list_movimientos:
            movimientos = list_movimientos()
        else:
            movimientos = _fetch_movimientos()
    except Exception as e:
        st.error(f"Error al obtener movimientos: {e}")

    if not movimientos:
        st.info("No hay movimientos registrados todavía.")
    else:
        st.table(movimientos)

    st.markdown("---")
    st.subheader("Añadir movimiento")

    with st.form("form_caja", clear_on_submit=True):
        id_ciclo = st.number_input("ID ciclo", min_value=1, value=1)
        tipo = st.selectbox("Tipo", ["ingreso", "egreso"])
        monto = st.number_input("Monto", min_value=0.0, format="%.2f", value=0.0)
        detalle = st.text_area("Detalle (opcional)")
        submit = st.form_submit_button("Agregar movimiento")

        if submit:
            try:
                if create_movimiento:
                    ok = create_movimiento(id_ciclo, tipo, monto, detalle)
                else:
                    ok = _insert_mov_direct(id_ciclo, tipo, monto, detalle)
                if ok:
                    st.success("Movimiento agregado.")
                    try:
                        st.experimental_rerun()
                    except Exception:
                        pass
                else:
                    st.error("No se pudo registrar el movimiento.")
            except Exception as ex:
                st.error(f"Error al agregar movimiento: {ex}")


