import streamlit as st
from modulos.config.conexion import test_connection
from modulos.db.crud_miembros import obtener_miembros

st.title("SGI — Proyecto Final")

ok, msg = test_connection()
if ok:
    st.success(msg)
else:
    st.error(msg)
    st.stop()

menu = st.sidebar.selectbox("Menú", ["Inicio", "Miembros"])
if menu == "Inicio":
    st.write("Bienvenido al sistema SGI-GAPC")
elif menu == "Miembros":
    st.header("Listado de miembros")
    st.write(obtener_miembros())

