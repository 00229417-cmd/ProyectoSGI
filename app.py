# app.py
import streamlit as st
from modulos.config.conexion import test_connection  # get_engine lo usan los CRUD/páginas
from modulos.login import login_page  # solo importamos la función de login (no circular)

st.set_page_config(
    page_title="GAPC Portal",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------
# CSS con paneles más anchos (mantener aspecto)
# ----------------------------
st.markdown(
    """
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
        box-shadow: 0 14px 40px rgba(60,103,214,0.18);
        animation: floaty 4.5s ease-in-out infinite;
    }
    @keyframes floaty {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-6px) scale(1.01); }
        100% { transform: translateY(0px); }
    }
    .header-title { color:#fff; margin:0; font-size:28px; font-weight:700; }
    .header-sub { color:#9FB4D6; font-size:13px; margin-top:4px; }
    .stTextInput>div>div>input {
        transition: box-shadow .18s ease, transform .18s ease;
        border-radius: 8px;
    }
    .stTextInput>div>div>input:focus {
        box-shadow: 0 8px 22px rgba(20,60,120,0.18);
        transform: translateY(-2px);
        outline: none;
    }
    .stButton>button {
        transition: transform .12s ease, box-shadow .12s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(20,60,120,0.12); }

    /* ancho mayor para dataframes/tablas dentro de la card */
    .center-card .stDataFrame, .center-card .stTable {
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# header + open card
st.markdown(
    """
    <div class="center-card">
      <div class="header-row">
        <div class="avatar-g">G</div>
        <div>
          <div class="header-title">GAPC — Portal</div>
          <div class="header-sub">Sistema de Gestión para Grupos de Ahorro y Préstamo Comunitarios</div>
        </div>
      </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# SESSIONS
# ----------------------------
st.session_state.setdefault("session_iniciada", False)
st.session_state.setdefault("usuario", None)
st.session_state.setdefault("user_role", None)

# ----------------------------
# Mostrar login si no hay sesión
# ----------------------------
if not st.session_state["session_iniciada"]:
    # muestra el login (login_page debe establecer st.session_state["session_iniciada"]=True al autenticar)
    try:
        login_page()
    except Exception as e:
        st.error(f"Error al cargar la pantalla de login: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    # cerrar la card y detener la ejecución hasta que el usuario se loguee
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()  # <-- FIX definitivo: corta la ejecución aquí hasta que session_iniciada True

# ----------------------------
# POST LOGIN
# ----------------------------
with st.sidebar:
    st.title("Menú")
    opcion = st.selectbox(
        "Ir a:",
        [
            "Dashboard",
            "Miembros",
            "Aportes",
            "Préstamos",
            "Cuotas",
            "Caja",
            "Reuniones",
            "Asistencia",
            "Multas",
            "Cierres",
            "Promotoras",
            "Ciclos",
            "Grupos",
            "Reportes",
            "Configuración",
        ],
    )
    st.divider()
    st.caption(f"Usuario: {st.session_state.get('usuario') or '—'}")
    if st.button("Cerrar sesión 🔒"):
        st.session_state["session_iniciada"] = False
        st.session_state["usuario"] = None
        st.session_state["user_role"] = None
        try:
            if hasattr(st, "experimental_rerun") and callable(st.experimental_rerun):
                st.experimental_rerun()
        except Exception:
            st.experimental_set_query_params(_reload="1")

# Test DB (opcional)
ok, msg = test_connection()
if not ok:
    st.warning(f"DB: NO CONECTADO ({msg})")
else:
    st.success("DB conectado")

# ----------------------------
# Helpers para import dinámico de páginas
# ----------------------------
def _import_and_call(module_path: str, func_names: list):
    """
    Importa dinamicamente module_path y llama la primera función encontrada en func_names.
    Retorna True si se llamó la página correctamente; si no, lanza excepción.
    """
    try:
        module = __import__(module_path, fromlist=["*"])
    except Exception as e:
        raise ImportError(f"Módulo {module_path} no encontrado: {e}") from e

    for fname in func_names:
        fn = getattr(module, fname, None)
        if callable(fn):
            fn()
            return True

    raise AttributeError(f"Ninguna de las funciones {func_names} está definida en {module_path}.")

# ----------------------------
# Páginas (carga dinámica)
# ----------------------------
try:
    if opcion == "Dashboard":
        _import_and_call("modulos.pages.dashboard_page", ["render_dashboard", "dashboard_page"])
    elif opcion == "Miembros":
        _import_and_call("modulos.pages.miembros_page", ["render_miembros", "miembros_page"])
    elif opcion == "Aportes":
        _import_and_call("modulos.pages.ahorro_page", ["render_ahorro", "ahorro_page"])
    elif opcion == "Préstamos":
        _import_and_call("modulos.pages.prestamos_page", ["render_prestamos", "prestamos_page"])
    elif opcion == "Cuotas":
        _import_and_call("modulos.pages.cuota_page", ["render_cuota", "cuota_page"])
    elif opcion == "Caja":
        _import_and_call("modulos.pages.caja_page", ["render_caja", "caja_page"])
    elif opcion == "Reuniones":
        _import_and_call("modulos.pages.reunion_page", ["render_reunion", "reunion_page"])
    elif opcion == "Asistencia":
        _import_and_call("modulos.pages.asistencia_page", ["render_asistencia", "asistencia_page"])
    elif opcion == "Multas":
        _import_and_call("modulos.pages.multas_page", ["render_multas", "multas_page"])
    elif opcion == "Cierres":
        _import_and_call("modulos.pages.cierre_page", ["render_cierre", "cierre_page"])
    elif opcion == "Promotoras":
        _import_and_call("modulos.pages.promotora_page", ["render_promotora", "promotora_page"])
    elif opcion == "Ciclos":
        _import_and_call("modulos.pages.ciclo_page", ["render_ciclo", "ciclo_page"])
    elif opcion == "Grupos":
        _import_and_call("modulos.pages.grupo_page", ["render_grupo", "grupo_page"])
    elif opcion == "Reportes":
        _import_and_call("modulos.pages.reporte_page", ["render_reporte", "reporte_page"])
    elif opcion == "Configuración":
        _import_and_call("modulos.pages.config_page", ["render_config", "config_page"])
    else:
        st.info("Opción no válida.")
except ImportError as ie:
    st.warning(f"Página no encontrada: {ie}")
    st.info("Verifica que el archivo exista en modulos/pages/ y que la función render_* esté definida.")
except AttributeError as ae:
    st.warning(f"Función de render no encontrada en módulo: {ae}")
except Exception as e:
    st.error(f"Error al cargar la página: {e}")

# cerrar card
st.markdown("</div>", unsafe_allow_html=True)



