# modulos/pages/reporte_page.py
import streamlit as st

def render_reporte():
    st.header("Generar reporte")

    # importar el CRUD localmente para evitar errores al importar el módulo si falta algo
    try:
        from modulos.db import crud_reporte
    except Exception as e:
        st.error(f"Error importando CRUD reporte: {e}")
        return

    # formulario para crear reporte
    with st.form("form_reporte"):
        # elegir tipo (ejemplo)
        tipo = st.selectbox("Tipo de reporte", ["mora", "balance", "cierre", "morosidad"])
        # id_ciclo — si no usas ciclos, dejar  NULL o 0
        id_ciclo = st.text_input("ID ciclo (opcional)", value="")
        id_adm = st.text_input("Usuario/ID administrador", value=st.session_state.get("usuario") or "")
        descripcion = st.text_area("Descripción (opcional)")

        enviar = st.form_submit_button("Generar reporte")

    if enviar:
        # validar id_ciclo si viene vacío -> None
        try:
            id_ciclo_val = int(id_ciclo) if id_ciclo.strip() != "" else None
        except ValueError:
            st.error("ID ciclo debe ser un número entero o dejarse vacío.")
            return

        # preparar params acorde a tu CRUD: (id_ciclo, id_administrador, tipo, descripcion)
        try:
            ok, msg = crud_reporte.create_reporte(id_ciclo_val, id_adm, tipo, descripcion)
            if ok:
                st.success("Reporte encolado/creado correctamente.")
            else:
                st.error(f"Error creando reporte: {msg}")
        except TypeError as te:
            st.error(f"Error guardando reporte: signature mismatch al llamar create_reporte: {te}")
        except Exception as e:
            st.error(f"Error al crear reporte: {e}")

