# app.py
import streamlit as st
from modulos.config.conexion import test_connection
from modulos.login import login_page

st.set_page_config(
    page_title="GAPC Portal",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# CSS — respetando tu diseño original
# =====================================================
st.markdown("""
<style>
.stApp {
    min-height: 100vh;
    background: linear-gradient(180deg, #071032 0%, #0b2248 45%, #041428 100%);
    background-attachment: fixed;
    display: flex;
    align-items: center;
    justify-content: center;
}
.center-card {
    width: min(1500px, 97%);
    margin: 20px auto;
    padding: 28px;
    border-radius: 14px;
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
    box-shadow: 0 18px 50px rgba(2,8,25,0.7);
    backdrop-filter: blur(6px) saturate(120%);
    border: 1px solid rgba(255,255,255,0.035);
}
.header-row { display:flex; gap:18px; align-items:center; margin-bottom:14px; }
.avatar-g {
    width:72px; height:72px; border-radius:14px;
    display:flex; align-items:center; justify-content:center;
    font-weight:800; color:white; font-size:30px;
    background: linear-gradient(135deg,#5b8bff,#3c67d6);
}
.header-title { color:#fff; margin:0; font-size:28px; font-weight:700; }
.header-sub { color:#9FB4D6; font-size:13px; margin-top:4px; }

.stTextInput>div>div>input, .stTextInput>div>div>textarea {
    transition: box-shadow .18s ease, transform .18s ease;
    border-radius: 8px;
}
.stTextInput>div>div>input:focus, .stTextInput>div>div>textarea:focus {
    box-shadow: 0 8px 22px rgba(20,60,120,0.18);
    transform: translateY(-2px);
    outline: none;
}

.stButton>button { transition: transform .12s ease, box-shadow .12s ease; }
.stButton>button:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(20,60,120,0.12); }

.center-card .stDataFrame, .center-card .stTable { width: 100% !important; }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------
# ENCABEZADO
# -----------------------------------------------------
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


# =====================================================
# SESIONES
# =====================================================
st.session_state.setdefault("session_iniciada", False)
st.session_state.setdefault("usuario", None)
st.session_state.setdefault("user_role", None)


# =====================================================
# LOGIN
# =====================================================
if not st.session_state["session_iniciada"]:
    try:
        login_page()
    except Exception as e:
        st.error(f"Error cargando login: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.markdown("## 🔧 Menú")

    ICONS = {
        "Dashboard": "📊",
        "Miembros": "👥",
        "Aportes": "💰",
        "Préstamos": "🏦",
        "Cuotas": "📅",
        "Caja": "🧾",
        "Reuniones": "🗓️",
        "Asistencia": "✅",
        "Multas": "⚖️",
        "Cierres": "🔒",
        "Promotoras": "📣",
        "Ciclos": "🔁",
        "Grupos": "🧩",
        "Reportes": "📄",
        "Configuración": "⚙️",
    }

    opciones = list(ICONS.keys())
    opcion = st.selectbox("Ir a:", opciones, format_func=lambda x: f"{ICONS[x]}  {x}")

    st.divider()
    st.caption(f"Usuario: {st.session_state.get('usuario') or '—'}")

    if st.button("Cerrar sesión 🔒"):
        st.session_state.clear()
        st.rerun()  # reemplazo seguro del deprecated experimental_rerun


# =====================================================
# MENSAJE ÚNICO DE DB
# =====================================================
ok, msg = test_connection()
if ok:
    st.caption("🟢 Conexión establecida")
else:
    st.caption(f"🔴 Error de conexión: {msg}")


# =====================================================
# IMPORTADOR DINÁMICO DE PÁGINAS
# =====================================================
def _import_and_call(module_path, func_names):
    module = __import__(module_path, fromlist=["*"])
    for fn in func_names:
        if hasattr(module, fn):
            return getattr(module, fn)()
    raise AttributeError(f"Ninguna de las funciones {func_names} existe en {module_path}")


# =====================================================
# RUTEO DE PÁGINAS (CORREGIDO)
# =====================================================
try:
    routes = {
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

    modulo, funciones = routes[opcion]
    _import_and_call(modulo, funciones)

except Exception as e:
    st.error(f"Error cargando la página: {e}")


st.markdown("</div>", unsafe_allow_html=True)

