# app.py
import streamlit as st
from modulos.config.conexion import test_connection  # get_engine lo usan los CRUD
from modulos.login import login_page  # solo importar, login_page maneja forms / session

st.set_page_config(
    page_title="GAPC Portal",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------
# CSS - fondo degradado + contenedor ancho
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

    /* Inputs animados */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        transition: box-shadow .18s ease, transform .18s ease;
        border-radius: 8px;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        box-shadow: 0 8px 22px rgba(20,60,120,0.18);
        transform: translateY(-2px);
        outline: none;
    }

    /* botones con micro-animacion */
    .stButton>button {
        transition: transform .12s ease, box-shadow .12s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(20,60,120,0.12); }

    /* ancho mayor para formularios/panels internos (si quieres más ampliar) */
    .stApp .main .block-container {
        max-width: 1400px;
        padding-left: 40px;
        padding-right: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# header (tarjeta principal abierta)
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
# SESSION DEFAULTS
# ----------------------------
st.session_state.setdefault("session_iniciada", False)
st.session_state.setdefault("usuario", None)
st.session_state.setdefault("user_role", None)

# ----------------------------
# MOSTRAR LOGIN si no hay sesión
# ----------------------------
# login_page() debe: renderizar form, crear usuario si se solicita y, al login correcto,
# setear st.session_state["session_iniciada"]=True y st.session_state["usuario"]=username
if not st.session_state["session_iniciada"]:
    # muestra el login (login_page hace set en session_state y llama a rerun si implementado)
    login_page()
    # cerramos la tarjeta y detenemos la ejecución hasta que inicie sesión
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ----------------------------
# POST-LOGIN -> SIDEBAR y contenido
# ----------------------------
with st.sidebar:
    st.title("Menú")
    opcion = st.selectbox("Ir a:", ["Dashboard", "Miembros", "Aportes", "Préstamos", "Caja", "Reportes"])
    st.divider()
    st.caption(f"👤 Usuario: {st.session_state.get('usuario') or '—'}")
    if st.button("Cerrar sesión"):
        # limpiar sesión y forzar recarga
        st.session_state["session_iniciada"] = False
        st.session_state["usuario"] = None
        st.session_state["user_role"] = None
        try:
            if hasattr(st, "experimental_rerun") and callable(st.experimental_rerun):
                st.experimental_rerun()
        except Exception:
            # fallback: reload via small JS
            st.markdown(
                """<script>setTimeout(function(){ window.location.reload(); }, 200);</script>""",
                unsafe_allow_html=True,
            )

# Test DB (solo estado, no mostrar detalles)
ok, msg = test_connection()
if ok:
    st.success("✅ DB conectado")
else:
    st.warning(f"⚠️ DB: NO CONECTADO — {msg}")

# ----------------------------
# PÁGINAS: intento de importar módulo real (modulos/pages/<page>_page.py)
# Si no existe, muestro placeholder limpio
# ----------------------------
if opcion == "Dashboard":
    try:
        from modulos.pages.dashboard_page import render_dashboard
        render_dashboard()
    except Exception:
        st.info("Página 'Dashboard' (módulo modulos.pages.dashboard_page) no encontrada — mostrando placeholder.")
        st.header("Dashboard — Resumen operativo")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total miembros", "—")
        c2.metric("Préstamos vigentes", "—")
        c3.metric("Saldo caja", "—")
        st.subheader("Actividad reciente")
        st.table([])

elif opcion == "Miembros":
    try:
        from modulos.pages.miembros_page import render_miembros
        render_miembros()
    except Exception:
        st.error("Error al cargar la página 'Miembros' — usando placeholder.")
        st.header("Miembros")
        st.subheader("Lista de miembros registrados")
        st.info("No hay miembros registrados todavía o la página no está implementada.")
        st.table([])

elif opcion == "Aportes":
    try:
        from modulos.pages.aportes_page import render_aportes
        render_aportes()
    except Exception:
        st.header("Aportes")
        st.info("Registrar aportes (módulo no encontrado).")

elif opcion == "Préstamos":
    try:
        from modulos.pages.prestamos_page import render_prestamos
        render_prestamos()
    except Exception:
        st.header("Préstamos")
        st.info("Solicitudes y pagos (módulo no encontrado).")

elif opcion == "Caja":
    try:
        from modulos.pages.caja_page import render_caja
        render_caja()
    except Exception:
        st.header("Caja")
        st.info("Movimientos de caja (módulo no encontrado).")

elif opcion == "Reportes":
    try:
        from modulos.pages.reportes_page import render_reportes
        render_reportes()
    except Exception:
        st.header("Reportes")
        st.info("Exportar PDF / Excel (módulo no encontrado).")

# cerrar tarjeta principal
st.markdown("</div>", unsafe_allow_html=True)

