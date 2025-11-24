# app.py
import streamlit as st
import importlib
import traceback
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
""",
    unsafe_allow_html=True,
)


# -----------------------------------------------------
# ENCABEZADO
# -----------------------------------------------------
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
        # login_page debe setear st.session_state["session_iniciada"]=True y st.session_state["usuario"]
        login_page()
    except Exception as e:
        st.error(f"Error cargando login: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    # detener ejecución hasta que el usuario haga login
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
    # mostramos el icono + texto en el selectbox
    opcion = st.selectbox("Ir a:", opciones, format_func=lambda x: f"{ICONS.get(x,'')}  {x}")

    st.divider()
    st.caption(f"Usuario: {st.session_state.get('usuario') or '—'}")

    if st.button("Cerrar sesión 🔒"):
        # limpiar sesión y rerun (Streamlit 1.30+)
        st.session_state.clear()
        try:
            st.rerun()
        except Exception:
            # fallback seguro
            st.experimental_set_query_params(_logout="1")
            st.stop()


# =====================================================
# MENSAJE ÚNICO DE DB
# =====================================================
ok, msg = test_connection()
if ok:
    st.caption("🟢 Conexión establecida")
else:
    st.caption(f"🔴 Error de conexión: {msg}")


# =====================================================
# IMPORTADOR DINÁMICO DE PÁGINAS (robusto)
# =====================================================
def _import_and_call(module_path: str, func_names: list):
    """
    Intenta importar module_path y llamar la primera función disponible en func_names.
    Devuelve True si se ejecutó correctamente, False si hubo problema (ya mostrado).
    """
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError:
        st.warning(f"Página no encontrada: {module_path} (archivo faltante).")
        return False
    except Exception as e:
        st.error(f"Error importando módulo {module_path}: {e}")
        st.text(traceback.format_exc())
        return False

    for fname in func_names:
        fn = getattr(module, fname, None)
        if callable(fn):
            try:
                fn()
                return True
            except Exception as e:
                st.error(f"Error dentro de {module_path}.{fname}: {e}")
                st.text(traceback.format_exc())
                return False

    st.info(f"El módulo {module_path} existe pero no define ninguna de: {func_names}")
    return False


# =====================================================
# RUTEO DE PÁGINAS (con placeholders si falta)
# =====================================================
routes = {
    "Dashboard": ("modulos.pages.dashboard_page", ["render_dashboard", "dashboard_page"]),
    "Miembros": ("modulos.pages.miembros_page", ["render_miembros", "miembros_page"]),
    "Aportes": ("modulos.pages.aportes_page", ["render_aportes", "aportes_page", "ahorro_page", "render_ahorro"]),
    "Préstamos": ("modulos.pages.prestamos_page", ["render_prestamos", "prestamos_page"]),
    "Cuotas": ("modulos.pages.cuota_page", ["render_cuota", "cuota_page"]),
    "Caja": ("modulos.pages.caja_page", ["render_caja", "caja_page"]),
    "Reuniones": ("modulos.pages.reunion_page", ["render_reunion", "reunion_page"]),
    "Asistencia": ("modulos.pages.asistencia_page", ["render_asistencia", "asistencia_page"]),
    "Multas": ("modulos.pages.multas_page", ["render_multas", "multas_page"]),
    "Cierres": ("modulos.pages.cierre_page", ["render_cierre", "cierre_page"]),
    "Promotoras": ("modulos.pages.promotora_page", ["render_promotora", "promotora_page"]),
    "Ciclos": ("modulos.pages.ciclo_page", ["render_ciclo", "ciclo_page"]),
    "Grupos": ("modulos.pages.grupo_page", ["render_grupo", "grupo_page"]),
    "Reportes": ("modulos.pages.reporte_page", ["render_reporte", "reporte_page"]),
    "Configuración": ("modulos.pages.config_page", ["render_config", "config_page"]),
}

try:
    if opcion in routes:
        modpath, fnames = routes[opcion]
        ok_page = _import_and_call(modpath, fnames)
        if not ok_page:
            # placeholder amigable si la página no existe o falló
            st.header(f"{opcion} — (placeholder)")
            st.info(f"La página '{opcion}' aún no está disponible o falló al cargar. Verifica el archivo: {modpath.replace('.', '/')}.py")
            # algunas páginas pueden mostrar tablas vacías o botones para avanzar
            if opcion == "Miembros":
                st.write("Si 'Miembros' falló pero el CRUD está listo, revisa `modulos/db/crud_miembros.py` y asegura las funciones exportadas `obtener_miembros`, `create_miembro`, etc.")
    else:
        st.info("Opción no válida.")
except Exception as e:
    st.error(f"Error cargando la página: {e}")
    st.text(traceback.format_exc())


# =====================================================
# CIERRE DEL CARD
# =====================================================
st.markdown("</div>", unsafe_allow_html=True)


