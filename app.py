# app.py
import streamlit as st
import pandas as pd
from sqlalchemy import text
from modulos.config.conexion import test_connection, get_engine
from modulos.login import login_page

st.set_page_config(page_title="GAPC Portal", layout="wide", initial_sidebar_state="expanded")

# ----------------------------
# CSS / estilo (mantener apariencia)
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
# SESIONES
# ----------------------------
st.session_state.setdefault("session_iniciada", False)
st.session_state.setdefault("usuario", None)
st.session_state.setdefault("user_role", None)

# Si no hay sesión: mostrar login y detener ejecución
if not st.session_state["session_iniciada"]:
    try:
        login_page()  # debe establecer session_iniciada a True al autenticar
    except Exception as e:
        st.error(f"Error al cargar la pantalla de login: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    # cerramos la card y detenemos hasta que session_iniciada sea True
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ----------------------------
# POST-LOGIN: barra lateral y selección de página
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
            "Usuarios",
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
# Lista de tablas conocidas (ajusta si tu nombre real difiere)
# ----------------------------
TABLE_MAP = {
    "Dashboard": None,
    "Miembros": "miembro",
    "Aportes": "aporte",
    "Préstamos": "prestamo",
    "Cuotas": "cuota",
    "Caja": "caja",
    "Reuniones": "reunion",
    "Asistencia": "asistencia",
    "Multas": "multa",
    "Cierres": "cierre",
    "Promotoras": "promotora",
    "Ciclos": "ciclo",
    "Grupos": "grupo",
    "Reportes": "reporte",
    "Usuarios": "users",
    "Configuración": None,
}

# ----------------------------
# Función genérica que muestra la tabla (safe)
# ----------------------------
def render_table_from_db(table_name: str, limit: int = 200):
    st.subheader(f"Tabla: {table_name}  ⚡")
    engine = get_engine()
    q_text = f"SELECT * FROM {table_name} LIMIT :lim"
    try:
        with engine.connect() as conn:
            q = text(q_text)
            rows = conn.execute(q, {"lim": limit}).mappings().all()
            if not rows:
                st.info("No hay registros (vacío) o no se devolvieron filas.")
                return
            df = pd.DataFrame(rows)
            st.dataframe(df)  # muestra interactiva
    except Exception as e:
        # Mostrar error SQL completo para que lo copies y lo arreglemos
        st.error(f"Error al ejecutar la consulta en '{table_name}': {e}")
        st.caption("Revisa que la tabla/columnas existan en la base de datos remota y que los nombres coincidan exactamente.")

# ----------------------------
# Comportamiento por página (genérico)
# ----------------------------
if opcion == "Dashboard":
    st.header("Dashboard — Resumen operativo")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total miembros", "—")
    c2.metric("Préstamos vigentes", "—")
    c3.metric("Saldo caja", "—")
    st.subheader("Actividad reciente")
    st.table([])

elif opcion in TABLE_MAP:
    tbl = TABLE_MAP[opcion]
    if tbl is None:
        st.info(f"Página '{opcion}' — aquí irá la interfaz completa (formulario / reportes).")
    else:
        # tratamiento especial para USERS (muestro columnas esperadas)
        if tbl == "users":
            st.header("Usuarios — gestión")
            st.write("Mostrando columnas principales (id, username, full_name, email, role, created_at)")
            engine = get_engine()
            q = text("SELECT id, username, full_name, email, role, created_at FROM users LIMIT :lim")
            try:
                with engine.connect() as conn:
                    rows = conn.execute(q, {"lim": 200}).mappings().all()
                    if not rows:
                        st.info("No hay usuarios registrados.")
                    else:
                        df = pd.DataFrame(rows)
                        st.dataframe(df)
            except Exception as e:
                st.error(f"Error al consultar 'users': {e}")
                st.caption("Si la tabla existe pero la consulta falla, puede ser que los nombres de columna sean distintos. Muestra el error completo y lo corrijo.")
        else:
            # Genérico: listar la tabla completa (SELECT * LIMIT)
            render_table_from_db(tbl)

else:
    st.info("Opción no implementada todavía.")

# cerrar card
st.markdown("</div>", unsafe_allow_html=True)

