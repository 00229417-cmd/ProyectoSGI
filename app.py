# app.py (entrada principal)
import streamlit as st
from modulos.config.conexion import test_connection, get_engine

st.set_page_config(page_title="GAPC Portal", layout="wide", initial_sidebar_state="expanded")

st.session_state.setdefault("session_iniciada", False)
st.session_state.setdefault("usuario", None)
st.session_state.setdefault("user_role", None)

# Si no está autenticado -> mostrar login y detener
if not st.session_state["session_iniciada"]:
    from modulos.login import login_page
    login_page()
    st.stop()

# Si llegó hasta aquí: sesión activa
with st.sidebar:
    st.title("Menú")
    opcion = st.selectbox("Ir a:", ["Dashboard", "Miembros", "Aportes", "Préstamos", "Caja", "Reportes"])
    st.divider()
    st.caption(f"Usuario: {st.session_state.get('usuario')}")
    if st.button("Cerrar sesión"):
        st.session_state["session_iniciada"] = False
        st.session_state["usuario"] = None
        st.session_state["user_role"] = None
        st.experimental_rerun()

# Header premium
st.markdown("""
<div style="display:flex;align-items:center;gap:18px">
  <div style="width:72px;height:72px;border-radius:12px;background:linear-gradient(135deg,#5b8bff,#3c67d6);display:flex;align-items:center;justify-content:center;font-weight:800;color:white;font-size:28px;box-shadow:0 20px 40px rgba(0,0,0,0.45);">G</div>
  <div>
    <h1 style="margin:0;color:#fff">GAPC — Portal</h1>
    <div style="color:#9FB4D6">Sistema de Gestión para Grupos de Ahorro y Préstamo Comunitarios</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Test conexion (opcional, quita en prod)
ok, msg = test_connection()
if not ok:
    st.warning(f"DB: NO CONECTADO ({msg})")
else:
    st.success("DB conectado")

# Páginas
if opcion == "Dashboard":
    st.header("Dashboard — Resumen operativo")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total miembros", "—")
    c2.metric("Préstamos vigentes", "—")
    c3.metric("Saldo caja", "—")
    st.subheader("Actividad reciente")
    st.table([])

elif opcion == "Miembros":
    st.header("Miembros")
    st.info("Aquí puedes listar/crear/editar miembros (implementar).")

elif opcion == "Aportes":
    st.header("Aportes")
    st.info("Registrar aportes por reunión / grupo (implementar).")

elif opcion == "Préstamos":
    st.header("Préstamos")
    st.info("Solicitudes y pagos (implementar).")

elif opcion == "Caja":
    st.header("Caja")
    st.info("Movimientos de caja (implementar).")

elif opcion == "Reportes":
    st.header("Reportes")
    st.info("Exportar PDF / Excel (implementar).")




