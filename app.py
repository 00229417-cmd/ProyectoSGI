# app.py (fragmento para integrar la guía visual)
import streamlit as st
from modulos.config.conexion import test_connection
from modulos.auth.auth import init_session, create_user_table_if_not_exists, login_form, register_form, logout

# inicializa auth table
create_user_table_if_not_exists()
init_session()

st.set_page_config(page_title="SGI GAPC", layout="wide")
st.title("SGI — Portal")

# Autenticación
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

# Menú principal
menu = st.sidebar.radio("Navegación", ["Dashboard", "Guía visual", "Miembros", "Aportes", "Préstamos", "Reportes"])

if menu == "Guía visual":
    from modulos.ui_components.guide_page import render_guide_page
    render_guide_page()

# (mantén o añade los otros menús como desees)

