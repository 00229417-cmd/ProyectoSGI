# app.py (entrada principal)
import streamlit as st
from modulos.config.conexion import test_connection, test_connection_verbose

st.set_page_config(page_title="GAPC Portal", layout="wide", initial_sidebar_state="expanded")

# ------------------------------
# Fondo degradado azul (no cambia layout/controles)
# ------------------------------
st.markdown(
    """
    <style>
    /* fondo degradado completo */
    .stApp {
        background: linear-gradient(180deg, #071032 0%, #0b2248 35%, #09203d 100%);
        background-attachment: fixed;
    }

    /* opcional: caja principal translúcida */
    .main > div[role="main"] {
        backdrop-filter: blur(6px) saturate(120%);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Control de sesión
# ------------------------------
st.session_state.setdefault("session_iniciada", False)
st.session_state.setdefault("usuario", None)
st.session_state.setdefault("user_role", None)

# Si no está autenticado, mostrar login
if not st.session_state["session_iniciada"]:
    from modulos.login import login_page
    login_page()
    st.stop()

# =====================================================
# SIDEBAR (MENÚ Y DIAGNÓSTICO)
# =====================================================
with st.sidebar:
    st.title("Menú")
    opcion = st.selectbox("Ir a:", ["Dashboard", "Miembros", "Aportes", "Préstamos", "Caja", "Reportes"])

    st.divider()

    st.caption(f"Usuario: {st.session_state.get('usuario')}")

    # ---------- Botón de diagnóstico DB ----------
    if st.button("🔧 Diagnóstico DB", use_container_width=True):
        ok_verbose, msg_verbose = test_connection_verbose()
        if ok_verbose:
            st.success("Base de datos conectada correctamente.")
        else:
            st.error("❌ Error de conexión a la BD")
            with st.expander("Ver detalle del error técnico"):
                st.write(msg_verbose)

    # ---------- Enlace discreto al ER local ----------
    ER_LOCAL_PATH = "/mnt/data/ER proyecto - ER NUEVO.png"
    st.markdown(f"[📄 Ver diagrama ER]({ER_LOCAL_PATH})", unsafe_allow_html=True)

    st.divider()

    # Botón cerrar sesión
    if st.button("Cerrar sesión", use_container_width=True):
        st.session_state["session_iniciada"] = False
        st.session_state["usuario"] = None
        st.session_state["user_role"] = None
        st.experimental_rerun()

# =====================================================
# HEADER PREMIUM
# =====================================================
st.markdown("""
<div style="display:flex;align-items:center;gap:18px">
  <div style="width:72px;height:72px;border-radius:12px;background:linear-gradient(135deg,#5b8bff,#3c67d6);display:flex;align-items:center;justify-content:center;font-weight:800;color:white;font-size:28px;box-shadow:0 20px 40px rgba(0,0,0,0.45);">G</div>
  <div>
    <h1 style="margin:0;color:#fff">GAPC — Portal</h1>
    <div style="color:#9FB4D6">Sistema de Gestión para Grupos de Ahorro y Préstamo Comunitarios</div>
  </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# TEST DE CONEXIÓN (RÁPIDO) — NO CAMBIADO
# =====================================================
ok = test_connection()
if not ok:
    st.warning("DB: NO CONECTADO")
else:
    st.success("DB conectado")


# =====================================================
# PÁGINAS (CONTENIDO)
# =====================================================
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





