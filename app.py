# app.py — GAPC Portal (versión PREMIUM corregida)
# - Primera línea: IMPORTS (NADA antes de esto)
import streamlit as st

# Configuración inicial de la página
st.set_page_config(page_title="GAPC Portal", layout="wide", initial_sidebar_state="expanded")

# -------------------------
# Inicializar session_state
# -------------------------
st.session_state.setdefault("session_iniciada", False)
st.session_state.setdefault("usuario", None)
st.session_state.setdefault("usuario_id", None)
st.session_state.setdefault("user_role", None)
st.session_state.setdefault("mostrar_registro_sidebar", False)

# -------------------------
# Ruta local al ER (archivo subido)
# -------------------------
# (esta ruta se corresponde con el archivo que tú subiste al workspace)
ER_LOCAL_URL = "file:///mnt/data/ER proyecto - ER NUEVO.png"

# -------------------------
# Importar módulos (después de inicializar session_state)
# -------------------------
# login_page debe ocultar/mostrar login y al autenticar setear:
# st.session_state["session_iniciada"] = True
# st.session_state["usuario"] = username
# st.session_state["usuario_id"] = id
# st.session_state["user_role"] = role
try:
    from modulos.login import login_page
except Exception:
    # Fallback: si el módulo no existe, definimos una función minimal
    def login_page():
        st.error("módulo modulos.login no encontrado. Crea modulos/login.py")

# Funciones auxiliares para crear usuarios admin desde sidebar
try:
    from modulos.db.crud_users import create_user_and_member
except Exception:
    def create_user_and_member(*args, **kwargs):
        st.error("create_user_and_member no disponible (modulos/db/crud_users.py faltante).")
        return None

# -------------------------
# Si no hay sesión: mostrar login (modular) y detener ejecución
# -------------------------
if not st.session_state["session_iniciada"]:
    # login_page debe manejar login + registro apilado/expander
    login_page()
    st.stop()

# -------------------------
# Si hay sesión: mostrar la app principal con sidebar
# -------------------------
# Sidebar: menú, info de usuario, registro admin (si corresponde)
with st.sidebar:
    st.markdown("## Menú 📋")
    opcion = st.selectbox("Selecciona una opción", ["Dashboard", "Miembros", "Aportes", "Préstamos", "Caja", "Reportes"])
    st.divider()
    st.caption(f"Conectado: **{st.session_state.get('usuario') or '—'}**")

    # Mostrar registro en sidebar SOLO para admins
    user_role = st.session_state.get("user_role")
    if user_role == "admin":
        st.markdown("### Registro (admin)")
        with st.expander("Crear usuario / miembro"):
            ru = st.text_input("Usuario (nuevo)", key="side_ru")
            rn = st.text_input("Nombre completo", key="side_rn")
            rd = st.text_input("Identificación (opcional)", key="side_rd")
            rt = st.text_input("Teléfono (opcional)", key="side_rt")
            rdir = st.text_input("Dirección (opcional)", key="side_rdir")
            rpw = st.text_input("Contraseña", type="password", key="side_rpw")
            rpw2 = st.text_input("Confirmar contraseña", type="password", key="side_rpw2")
            if st.button("Crear usuario (admin)", use_container_width=True):
                if not ru or not rpw:
                    st.error("Usuario y contraseña requeridos.")
                elif rpw != rpw2:
                    st.error("Contraseñas no coinciden.")
                else:
                    uid = create_user_and_member(
                        username=ru,
                        password=rpw,
                        full_name=rn,
                        dni=rd,
                        telefono=rt,
                        direccion=rdir,
                        role="user",
                    )
                    if uid:
                        st.success("Usuario y miembro creados correctamente.")
                    else:
                        st.error("Error al crear usuario/miembro.")

    st.divider()
    if st.button("Cerrar sesión 🔒", use_container_width=True):
        # limpiar sesión y recargar
        st.session_state["session_iniciada"] = False
        st.session_state["usuario"] = None
        st.session_state["usuario_id"] = None
        st.session_state["user_role"] = None
        try:
            st.rerun()
        except Exception:
            st.experimental_rerun()

# -------------------------
# Main area: páginas según opción
# -------------------------
# Encabezado premium (marca / avatar)
st.markdown(
    """
    <style>
    .brand-row { display:flex; gap:18px; align-items:center; margin-bottom:6px; }
    .logo-box { width:72px; height:72px; border-radius:14px; background: linear-gradient(135deg,#5b8bff,#3c67d6); display:flex;align-items:center;justify-content:center;color:white;font-weight:800;font-size:26px; box-shadow: 0 12px 36px rgba(0,0,0,0.45); animation: floaty 6s ease-in-out infinite; }
    @keyframes floaty { 0%{transform:translateY(0)}50%{transform:translateY(-6px)}100%{transform:translateY(0)} }
    .brand-title { font-size:30px; margin:0; color:#F7FBFF; }
    .brand-sub { color:#9FB4D6; margin-top:6px; font-size:13px; }
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([0.12, 1])
with col1:
    st.markdown('<div class="logo-box">G</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="brand-title">GAPC — Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Sistema de Gestión para Grupos de Ahorro y Préstamo Comunitarios</div>', unsafe_allow_html=True)

# -------------------------
# Páginas (esqueleto: reemplaza con tus páginas reales)
# -------------------------
if opcion == "Dashboard":
    st.header("Dashboard — Resumen operativo")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total miembros", "—")
        st.write("Ahorros totales: —")
    with c2:
        st.metric("Préstamos vigentes", "—")
        st.write("Mora (%): —")
    with c3:
        st.metric("Saldo caja", "—")
        st.write("Próximos cierres: —")

    st.markdown("---")
    st.subheader("Actividad reciente")
    st.table([{"evento": "Pago", "miembro": "Juan", "monto": "$20"}, {"evento": "Aporte", "miembro": "Ana", "monto": "$5"}])

elif opcion == "Miembros":
    st.header("Miembros")
    st.info("Aquí se mostrará la lista de miembros y acciones CRUD (crear/editar/eliminar).")
    # si tienes un módulo real: from modulos.miembros.page import mostrar_miembros

elif opcion == "Aportes":
    st.header("Aportes")
    st.info("Gestión de aportes — registrar y visualizar aportes por reunión/grupo.")

elif opcion == "Préstamos":
    st.header("Préstamos")
    st.info("Solicitudes, aprobación, calendario de cuotas y pagos.")

elif opcion == "Caja":
    st.header("Caja")
    st.info("Movimientos de caja, cierre y balance.")

elif opcion == "Reportes":
    st.header("Reportes")
    st.info("Generación de reportes operativos y financieros.")

else:
    st.header(opcion)
    st.info("Sección en construcción.")

# -------------------------
# Botón discreto para abrir la documentación (ER) — esquina inferior derecha
# -------------------------
# Construimos HTML/CSS de forma segura (botón pequeño sin texto visible)
er_html = f'''
<style>
.er-button {{
    position: fixed;
    right: 18px;
    bottom: 18px;
    width:44px;
    height:44px;
    border-radius:10px;
    background: linear-gradient(135deg,#6fa8ff,#4a63d1);
    display:flex;
    align-items:center;
    justify-content:center;
    box-shadow:0 10px 28px rgba(0,0,0,0.45);
    z-index: 9999;
}}
.er-button svg {{ width:20px; height:20px; }}
</style>
<a href="{ER_LOCAL_URL}" target="_blank" class="er-button" title="Documentación (ER)">
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M7 2H13L18 7V22H7V2Z" fill="white" fill-opacity="0.95"/>
  <path d="M13 2V7H18" stroke="white" stroke-opacity="0.6" stroke-width="0.6"/>
</svg>
</a>
'''
st.components.v1.html(er_html, height=60)



