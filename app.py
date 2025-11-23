import streamlit as st
from modulos.config.conexion import test_connection
from modulos.auth.auth import (
    create_user_table_if_not_exists,
    init_session,
    login_form,
    register_form,
    logout,
)
from modulos.ui_components.guide_page import render_guide_page

create_user_table_if_not_exists()
init_session()

st.set_page_config(page_title="SGI GAPC", layout="wide")
st.title("SGI — Portal")

# Authentication area
if st.session_state.get("user") is None:
    col1, col2 = st.columns(2)
    with col1:
        ok = login_form()
        if ok:
            st.experimental_rerun()
    with col2:
        register_form()
    st.stop()
else:
    st.sidebar.write(f"Conectado: {st.session_state.user['username']}")
    if st.sidebar.button("Cerrar sesión"):
        logout()
        st.experimental_rerun()

# quick connection status
ok, msg = test_connection()
if ok:
    st.sidebar.success("DB: conectado")
else:
    st.sidebar.error("DB: no conectado")

menu = st.sidebar.radio("Navegación", ["Dashboard", "Guía visual", "Miembros", "Aportes", "Préstamos", "Reportes"])

if menu == "Guía visual":
    render_guide_page()
elif menu == "Dashboard":
    st.header("Dashboard (pendiente integrar)")
    st.write("Aquí irán KPIs y vistas principales.")
else:
    st.header(menu)
    st.write("Página en construcción: pronto aquí podrá gestionar", menu)


