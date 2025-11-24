# app.py (pegar reemplazando el archivo actual)
import streamlit as st
from importlib import import_module

# tu conexión / helpers
from modulos.config.conexion import test_connection

# página de login (debe existir)
from modulos.login import login_page

st.set_page_config(
    page_title="GAPC Portal",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------
# CSS con paneles más anchos + micro-animaciones
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

    /* ancho mayor para formularios dentro del card */
    .block-container .stForm {
        max-width: 900px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# header + card container abierto
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
# Mostrar login si no hay sesión (detiene ejecución)
# ----------------------------
if not st.session_state["session_iniciada"]:
    login_page()                     # el login debe modificar st.session_state["session_iniciada"]
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()                         # <- fix definitivo: corta aquí cuando no hay sesión

# ----------------------------
# Si llegamos hasta aquí la sesión está iniciada -> render app
# ----------------------------
with st.sidebar:
    st.title("Menú")
    opcion = st.selectbox(
        "Ir a:",
        ["Dashboard", "Miembros", "Aportes", "Préstamos", "Caja", "Reportes"]
    )
    st.divider()
    st.caption(f"Usuario: {st.session_state.get('usuario')}")
    if st.button("Cerrar sesión"):
        st.session_state["session_iniciada"] = False
        st.session_state["usuario"] = None
        st.session_state["user_role"] = None
        # forzar recarga para limpiar estado UI
        try:
            if hasattr(st, "experimental_rerun") and callable(st.experimental_rerun):
                st.experimental_rerun()
        except Exception:
            # fallback: pequeña redirección JS
            st.markdown(
                """<script>setTimeout(function(){ window.location.reload(); }, 150);</script>""",
                unsafe_allow_html=True,
            )

# Test de conexión (opcional)
ok, msg = test_connection()
if not ok:
    st.warning(f"DB: NO CONECTADO ({msg})")
else:
    st.success("DB conectado")

# ----------------------------
# RUTEO DE PÁGINAS (intenta importar módulo en modulos.pages)
# cada módulo recomendado: modulos/pages/<name>_page.py
# Debe exponer una función `render()` (preferible) o `run()`.
# ----------------------------
def run_page(module_name: str, fallback_title: str):
    """
    intenta importar modulos.pages.<module_name> y ejecutar render()/run().
    si falla, muestra un placeholder simple (tabla vacía).
    """
    full_module = f"modulos.pages.{module_name}_page"
    try:
        mod = import_module(full_module)
        # preferimos render(); si no existe, try run()
        if hasattr(mod, "render") and callable(mod.render):
            mod.render()
            return True
        elif hasattr(mod, "run") and callable(mod.run):
            mod.run()
            return True
        else:
            st.warning(f"El módulo {full_module} no expone render() ni run().")
    except ModuleNotFoundError:
        st.info(f"Página '{fallback_title}' (módulo {full_module}) no encontrada — mostrando placeholder.")
    except Exception as e:
        st.error(f"Error al cargar la página '{fallback_title}': {e}")

    # placeholder: tabla vacía y mensaje
    st.header(f"{fallback_title} — (placeholder)")
    st.write("Aún no hay implementación completa. Aquí irá la tabla con registros / CRUD.")
    st.dataframe([], use_container_width=True)
    return False

# ----------------------------
# Ejecutar página según selección
# ----------------------------
if opcion == "Dashboard":
    # intento de cargar modulos.pages.dashboard_page.render()
    run_page("dashboard", "Dashboard")

elif opcion == "Miembros":
    run_page("miembros", "Miembros")

elif opcion == "Aportes":
    run_page("aportes", "Aportes")

elif opcion == "Préstamos":
    run_page("prestamos", "Préstamos")

elif opcion == "Caja":
    run_page("caja", "Caja")

elif opcion == "Reportes":
    run_page("reportes", "Reportes")

# cerrar card
st.markdown("</div>", unsafe_allow_html=True)


