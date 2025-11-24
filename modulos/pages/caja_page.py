# modulos/pages/caja_page.py
import streamlit as st
from modulos.db.crud_caja import list_caja, create_caja

def safe_rerun():
    """
    Intenta rerun de forma compatible con distintas versiones de Streamlit.
    """
    try:
        return st.rerun()
    except Exception:
        try:
            return st.experimental_rerun()
        except Exception:
            # fallback ligero: fuerza recarga mediante query params
            try:
                st.experimental_set_query_params(_reload="1")
            except Exception:
                pass
            return

def _ensure_state_keys():
    st.session_state.setdefault("show_form_caja", False)
    st.session_state.setdefault("last_caja_created", None)

def render_caja():
    _ensure_state_keys()
    st.markdown("## 🧾 Caja")

    cols = st.columns([1, 5])
    with cols[0]:
        if st.button("➕ Nuevo movimiento en caja"):
            st.session_state["show_form_caja"] = not st.session_state["show_form_caja"]
    with cols[1]:
        st.write("")

    st.subheader("Movimientos recientes")
    try:
        filas = list_caja()
        if not filas:
            st.info("No hay movimientos en caja.")
        else:
            st.table(filas)
    except Exception as e:
        st.error(f"Error cargando movimientos: {e}")

    st.markdown("---")

    if st.session_state["show_form_caja"]:
        st.subheader("Registrar movimiento en caja")
        with st.form("form_caja"):
            id_ciclo = st.number_input("ID Ciclo (opcional)", min_value=0, value=0)
            id_ahorro = st.number_input("ID Ahorro (opcional)", min_value=0, value=0)
            id_prestamo = st.number_input("ID Préstamo (opcional)", min_value=0, value=0)
            id_pago = st.number_input("ID Pago (opcional)", min_value=0, value=0)
            saldo_inicial = st.number_input("Saldo inicial", format="%.2f", value=0.0)
            ingresos = st.number_input("Ingresos", format="%.2f", value=0.0)
            egresos = st.number_input("Egresos", format="%.2f", value=0.0)
            submitted = st.form_submit_button("Guardar movimiento")

        if submitted:
            try:
                # convert 0 -> None for optional FKs
                id_ciclo_val = int(id_ciclo) if id_ciclo and int(id_ciclo) > 0 else None
                id_ahorro_val = int(id_ahorro) if id_ahorro and int(id_ahorro) > 0 else None
                id_prestamo_val = int(id_prestamo) if id_prestamo and int(id_prestamo) > 0 else None
                id_pago_val = int(id_pago) if id_pago and int(id_pago) > 0 else None

                new_id = create_caja(
                    id_ciclo=id_ciclo_val,
                    id_ahorro=id_ahorro_val,
                    id_prestamo=id_prestamo_val,
                    id_pago=id_pago_val,
                    saldo_inicial=float(saldo_inicial),
                    ingresos=float(ingresos),
                    egresos=float(egresos),
                )
                if new_id:
                    st.success(f"Movimiento registrado. ID: {new_id}")
                    st.session_state["last_caja_created"] = new_id
                    safe_rerun()
                else:
                    st.error("No se pudo registrar el movimiento.")
            except Exception as e:
                st.error(f"Error guardando movimiento: {e}")


