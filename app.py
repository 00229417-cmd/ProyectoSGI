# app.py
import streamlit as st
from modulos.config.conexion import test_connection
from modulos.login import login_page

st.set_page_config(
    page_title="GAPC Portal",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================
#           CSS GLOBAL
# ==============================
st.markdown("""
<style>
.stApp {
    min-height: 100vh;
    background: linear-gradient(180deg, #071032 0%, #0b2248 45%, #041428 100%);
    background-attachment: fixed;
}
.center-card {
    width: min(1500px, 97%);
    margin: 20px auto;
    padding: 28px;
    border-radius: 14px;
    background: rgba(255,255,255,0.02);
    box-shadow: 0 18px 50px rgba(2,8,25,0.7);
    backdrop-filter: blur(6px) saturate(120%);
    border: 1px solid rgba(255,255,255,0.035);
}
.header-row {
    display:flex;
    gap:18px;
    align-items:center;
    margin-bottom:14px;
}
.avatar-g {
    width:72px; height:72px;
    border-radius:14px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:800;
    font-size:30px;
    color:white;
    background: linear-gradient(135deg,#5b8bff,#3c67d6);
}
.header-title { color:#fff; font-size:28px; font-weight:700; }
.header-sub { color:#9FB4D6; font-size:13px; margin-top:4px; }
</style>
""", unsafe_allow_html=True)

# ==============================
#      CONTENEDOR PRINCIPAL
# ==============================
st.markdown("""
<div class="center-card">
  <div class="header-row">
    <div class="avatar-g">G</div>
    <div>
      <div class="header-title">GAPC — Portal</div>
      <div class="header-sub">Sistema de Gestión para Grupos de Ahorro y Préstamo Comunitarios</div>
    </div>
  </div>
""", unsafe_allow_html=True)

# ==============================
#           SESIONES
# ==============================
st.session_state.setdefault("session_iniciada", False)
st.session_state.setdefault("usuario", None)

# ==============================
#          LOGIN
# ==============================
if not st.session_state["session_iniciada"]:
    login_page()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==============================
#       BARRA LATERAL
# ==============================
with st.sidebar:
    st.title("Menú")
    opcion = st.selectbox("Ir a:", [
        "Dashboard", "Miembros", "Aportes", "Préstamos",
        "Cuotas", "Caja", "Reuniones", "Asistencia",
        "Multas", "Cierres", "Promotoras", "Ciclos",
        "Grupos", "Reportes", "Configuración"
    ])
    st.caption(f"Usuario: {st.session_state['usuario'] or '—'}")

    if st.button("Cerrar sesión 🔒"):
        st.session_state.clear()
        st.experimental_rerun()

# ==============================
#   MENSAJE DE CONEXIÓN ÚNICO
# ==============================
ok, msg = test_connection()
if ok:
    st.caption("🟢 Conexión establecida")
else:
    st.caption("🔴 Error conectando a la base de datos")

# ==============================
#    IMPORTACIÓN DINÁMICA
# ==============================
def cargar(modulo, funciones):
    try:
        m = __import__(modulo, fromlist=["*"])
        for f in funciones:
            if hasattr(m, f):
                return getattr(m, f)()
        st.error(f"No existe función render en {modulo}")
    except Exception as e:
        st.error(f"Error cargando página: {e}")

# ==============================
#       RUTEO DE PÁGINAS
# ==============================
paginas = {
    "Dashboard": ("modulos.pages.dashboard_page", ["render_dashboard", "dashboard_page"]),
    "Miembros": ("modulos.pages.miembros_page", ["render_miembros"]),
    "Aportes": ("modulos.pages.aportes_page", ["render_aportes"]),
    "Préstamos": ("modulos.pages.prestamos_page", ["render_prestamos"]),
    "Cuotas": ("modulos.pages.cuota_page", ["render_cuota"]),
    "Caja": ("modulos.pages.caja_page", ["render_caja"]),
    "Reuniones": ("modulos.pages.reunion_page", ["render_reunion"]),
    "Asistencia": ("modulos.pages.asistencia_page", ["render_asistencia"]),
    "Multas": ("modulos.pages.multas_page", ["render_multas"]),
    "Cierres": ("modulos.pages.cierre_page", ["render_cierre"]),
    "Promotoras": ("modulos.pages.promotora_page", ["render_promotora"]),
    "Ciclos": ("modulos.pages.ciclo_page", ["render_ciclo"]),
    "Grupos": ("modulos.pages.grupo_page", ["render_grupo"]),
    "Reportes": ("modulos.pages.reporte_page", ["render_reporte"]),
    "Configuración": ("modulos.pages.config_page", ["render_config"]),
}

if opcion in paginas:
    cargar(*paginas[opcion])

st.markdown("</div>", unsafe_allow_html=True)
