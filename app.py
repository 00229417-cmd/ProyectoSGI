# app.py
import streamlit as st

# página y layout
st.set_page_config(page_title="GAPC Portal", layout="wide")

# inicializa session vars simples
st.session_state.setdefault("session_iniciada", False)
st.session_state.setdefault("usuario", None)
st.session_state.setdefault("usuario_id", None)

# ruta a tu ER/documentación (archivo subido)
logo_path = "file:///mnt/data/ER proyecto - ER NUEVO.png"

# Si no está iniciada la sesión: carga el login (modular)
if not st.session_state["session_iniciada"]:
    from modulos.login import login_page  # este módulo contiene login + registro premium
    login_page(logo_path=logo_path)       # al iniciar sesión el módulo hará st.session_state updates
    st.stop()

# Si llegamos aquí, hay sesión iniciada
with st.sidebar:
    st.header("Menú 📋")
    opcion = st.selectbox("Selecciona una opción", ["Dashboard", "Miembros", "Aportes", "Préstamos", "Caja", "Reportes"])
    st.divider()
    st.caption(f"Conectado: {st.session_state['usuario']}")
    if st.button("Cerrar sesión 🔒", use_container_width=True):
        # limpiar session
        st.session_state["session_iniciada"] = False
        st.session_state["usuario"] = None
        st.session_state["usuario_id"] = None
        st.rerun()

# rutas de páginas
if opcion == "Dashboard":
    st.title("Dashboard — Resumen operativo")
    # (aquí se muestran KPIs y movimientos; se implementa en modulos/ui_components o en CRUD)
    from modulos.ui_components.dashboard import render_dashboard
    render_dashboard()
elif opcion == "Miembros":
    from modulos.miembros.page import mostrar_miembros
    mostrar_miembros()
elif opcion == "Aportes":
    from modulos.aportes.page import mostrar_aportes
    mostrar_aportes()
elif opcion == "Préstamos":
    from modulos.prestamos.page import mostrar_prestamos
    mostrar_prestamos()
elif opcion == "Caja":
    from modulos.caja.page import mostrar_caja
    mostrar_caja()
elif opcion == "Reportes":
    from modulos.reports.page import mostrar_reportes
    mostrar_reportes()
else:
    st.title("⚙️ Otras funciones")
    st.info("Aquí puedes agregar reportes u otras secciones.")


