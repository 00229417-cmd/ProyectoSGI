# fragmento dentro de modulos/pages/reporte_page.py (ejemplo de uso)
import streamlit as st
from modulos.db import crud_reporte

def render_reporte():
    st.header("Reportes")
    # formulario simple
    with st.form("form_reporte"):
        id_ciclo = st.text_input("ID Ciclo (opcional)", value="")
        tipo = st.selectbox("Tipo", ["mora", "cierre", "balance", "morosidad"])
        descripcion = st.text_area("Descripción", value="")
        submitted = st.form_submit_button("Crear reporte")

    if submitted:
        # prioridad: usar id de administrador guardado en la sesión (int)
        id_admin_session = st.session_state.get("usuario_id")  # esto debe haberse guardado en el login
        if id_admin_session:
            id_adm_param = id_admin_session
        else:
            # fallback: pasar el username (guardado en session_state["usuario"])
            id_adm_param = st.session_state.get("usuario", "")

        res = crud_reporte.create_reporte(id_ciclo, id_adm_param, tipo, descripcion)
        if res.get("ok"):
            st.success(f"Reporte creado (id={res.get('id')})")
        else:
            st.error(res.get("msg"))

