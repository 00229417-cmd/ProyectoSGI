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

    /* ancho mayor para formularios/tablas dentro de la card (mejora visual) */
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

    # siempre cerrar la card y detener la ejecución hasta que el usuario se loguee
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()  # <-- FIX definitivo: corta la ejecución aquí hasta que session_iniciada True

# ----------------------------
# POST LOGIN
# ----------------------------
with st.sidebar:
    st.title("Menú")
    opcion = st.selectbox("Ir a:", ["Dashboard", "Miembros", "Aportes", "Préstamos", "Caja", "Reportes"])
    st.divider()
    st.caption(f"Usuario: {st.session_state.get('usuario')}")
    if st.button("Cerrar sesión"):
        st.session_state["session_iniciada"] = False
        st.session_state["usuario"] = None
        st.session_state["user_role"] = None
        # intentar rerun para refrescar; si falla, recarga por JS
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
# - Intentamos importar la página y una de dos nombres de función (compatibilidad)
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
# Páginas (carga dinámica, mensajes claros si faltan modulos)
# ----------------------------
if opcion == "Dashboard":
    try:
        # admite dos convenciones: render_dashboard() o dashboard_page()
        _import_and_call("modulos.pages.dashboard_page", ["render_dashboard", "dashboard_page"])
    except Exception as e:
        st.info("Página 'Dashboard' (módulo modulos.pages.dashboard_page) no encontrada — mostrando placeholder.")
        st.header("Dashboard — (placeholder)")
        st.subheader("Actividad reciente")
        st.table([])

elif opcion == "Miembros":
    try:
        # admite render_miembros() o render_miembros / miembros_page / render_miembros_page
        _import_and_call("modulos.pages.miembros_page", ["render_miembros", "miembros_page", "render_miembros_page"])
    except Exception as e:
        st.error("Error al cargar la página 'Miembros': revisa modulos/db/crud_miembros.py para imports circulares.")
        st.header("Miembros — (placeholder)")
        st.info("Aún no hay implementación completa. Aquí irá la tabla con registros / CRUD.")
        st.table([])

elif opcion == "Aportes":
    try:
        _import_and_call("modulos.pages.aportes_page", ["render_aportes", "aportes_page"])
    except Exception:
        st.header("Aportes")
        st.info("Página 'Aportes' no encontrada. Implementar modulos/pages/aportes_page.py")

elif opcion == "Préstamos":
    try:
        _import_and_call("modulos.pages.prestamos_page", ["render_prestamos", "prestamos_page"])
    except Exception:
        st.header("Préstamos")
        st.info("Página 'Préstamos' no encontrada. Implementar modulos/pages/prestamos_page.py")

elif opcion == "Caja":
    try:
        _import_and_call("modulos.pages.caja_page", ["render_caja", "caja_page"])
    except Exception:
        st.header("Caja")
        st.info("Página 'Caja' no encontrada. Implementar modulos/pages/caja_page.py")

elif opcion == "Reportes":
    try:
        _import_and_call("modulos.pages.reportes_page", ["render_reportes", "reportes_page"])
    except Exception:
        st.header("Reportes")
        st.info("Página 'Reportes' no encontrada. Implementar modulos/pages/reportes_page.py")

# cerrar card
st.markdown("</div>", unsafe_allow_html=True)


