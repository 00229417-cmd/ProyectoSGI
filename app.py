# app.py — GAPC Portal (versión final: login desaparece después de iniciar sesión,
# registro debajo del login, movimientos en la zona del logo, panel de ayuda en footer)
import streamlit as st
from werkzeug.security import check_password_hash
from typing import List, Dict
from sqlalchemy import text

# Importa tus módulos (deben existir en el repo)
from modulos.config.conexion import get_engine
from modulos.auth.auth import (
    create_user_table_if_not_exists,
    init_session,
    get_user_by_username,
    register_user,
    logout,
)
# render_guide_page es opcional — si no existe coméntalo
try:
    from modulos.ui_components.guide_page import render_guide_page
except Exception:
    def render_guide_page():
        st.info("Guía visual no encontrada.")

# Inicialización (asegura tabla de usuarios y session)
create_user_table_if_not_exists()
init_session()

# Ruta a tu ER (archivo subido) — USAR LA RUTA EXACTA en tu entorno:
logo_path = "/mnt/data/ER proyecto - ER NUEVO.png"

# Configuración de la página
st.set_page_config(page_title="GAPC Portal", layout="wide", initial_sidebar_state="collapsed")

# --------------------------
# CSS ULTRA PREMIUM
# --------------------------
st.markdown(
    """
    <style>
    header { visibility: hidden; }
    main { padding-top: 0rem; }

    .stApp {
      background: linear-gradient(180deg,#071528 0%, #030915 100%);
      color: #EAF2FF;
      font-family: Inter, "Segoe UI", Roboto, Arial, sans-serif;
    }

    /* CONTAINER PRINCIPAL: arriba, no centrado verticalmente */
    .wrap {
      display:flex;
      justify-content:center;
      padding: 26px 12px 80px 12px;
      margin-top: 6px;
    }

    /* TARJETA PRINCIPAL */
    .card {
      width: 1000px;
      max-width: 98%;
      border-radius: 16px;
      padding: 24px;
      background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
      border: 1px solid rgba(255,255,255,0.04);
      box-shadow: 0 22px 60px rgba(0,0,0,0.55);
      display: grid;
      grid-template-columns: 1fr 360px;
      gap: 22px;
      margin-top: -36px; /* eleva ligeramente */
      animation: fadeIn 0.6s ease-out forwards;
    }
    @keyframes fadeIn {
      0% { opacity: 0; transform: translateY(12px); }
      100% { opacity: 1; transform: translateY(0); }
    }

    .logo-box {
      width:86px; height:86px; border-radius:16px;
      background: linear-gradient(135deg,#5b8bff,#3c67d6);
      display:flex; align-items:center; justify-content:center;
      color:white; font-weight:800; font-size:30px;
      box-shadow: 0 12px 36px rgba(40,80,200,0.30);
    }

    .brand-title { font-size:34px; margin:0; color:#F7FBFF; }
    .brand-sub { font-size:13px; color:#9FB4D6; margin-top:6px; }

    .login-title { font-size:20px; color:#EAF2FF; margin-top:6px; }
    .muted { color:#9FB4D6; font-size:13px; margin-bottom:10px; }

    .side-card { padding:14px; border-radius:12px; background: rgba(255,255,255,0.01); border:1px solid rgba(255,255,255,0.03); }

    .btn-ghost {
      background: transparent; border:1px solid rgba(255,255,255,0.06);
      color:#DCEBFF; padding:8px 10px; border-radius:10px;
    }

    .footer-help {
      margin-top: 18px;
      padding-top: 14px;
      border-top: 1px dashed rgba(255,255,255,0.03);
      color:#9FB4D6;
      font-size:13px;
    }

    @media (max-width: 900px) {
      .card { grid-template-columns: 1fr; margin-top: 0; }
      .logo-box { width:64px; height:64px; font-size:22px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------
# Helper: obtener movimientos recientes (intenta varias tablas)
# --------------------------
def fetch_recent_movements(limit: int = 6) -> List[Dict]:
    engine = None
    try:
        engine = get_engine()
    except Exception:
        engine = None

    queries = [
        "SELECT fecha as fecha, tipo_movimiento as tipo, monto, detalle FROM CajaMovimiento ORDER BY fecha DESC LIMIT :limit",
        "SELECT fecha as fecha, tipo as tipo, monto, detalle FROM caja_movimiento ORDER BY fecha DESC LIMIT :limit",
        "SELECT fecha as fecha, tipo as tipo, monto, detalle FROM caja ORDER BY fecha DESC LIMIT :limit",
        "SELECT fecha as fecha, 'movimiento' as tipo, monto, detalle FROM movimientos ORDER BY fecha DESC LIMIT :limit",
    ]

    if engine:
        for q in queries:
            try:
                with engine.connect() as conn:
                    res = conn.execute(text(q), {"limit": limit})
                    rows = res.fetchall()
                    if rows:
                        out = []
                        for r in rows:
                            try:
                                out.append(dict(r._mapping))
                            except Exception:
                                try:
                                    out.append(dict(r))
                                except Exception:
                                    out.append({
                                        "fecha": r[0] if len(r) > 0 else "",
                                        "tipo": r[1] if len(r) > 1 else "",
                                        "monto": r[2] if len(r) > 2 else "",
                                        "detalle": r[3] if len(r) > 3 else "",
                                    })
                        return out
            except Exception:
                continue

    # fallback: datos de ejemplo
    return [
        {"fecha": "2025-11-20", "tipo": "Aporte", "monto": 15.00, "detalle": "Aporte mensual - Juan"},
        {"fecha": "2025-11-19", "tipo": "Pago", "monto": 20.00, "detalle": "Pago cuota - María"},
        {"fecha": "2025-11-18", "tipo": "Retiro", "monto": 10.00, "detalle": "Retiro Fondo - Grupo A"},
    ]

# --------------------------
# MAIN LAYOUT: wrapper + card
# --------------------------
with st.container():
    st.markdown('<div class="wrap">', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # Layout: IZQUIERDA = contenido principal (login/reg/movimientos/dashboard),
    # DERECHA = espacio de ayuda reducida (ahora minimal)
    left_col, right_col = st.columns([2.1, 1])

    # ------------------ LEFT: Brand + LOGIN/REG o DASHBOARD ------------------
    with left_col:
        # Branding header (logo + title)
        brand_cols = st.columns([0.14, 1])
        with brand_cols[0]:
            st.markdown('<div class="logo-box">G</div>', unsafe_allow_html=True)
        with brand_cols[1]:
            st.markdown('<div class="brand-title">GAPC — Portal</div>', unsafe_allow_html=True)
            st.markdown('<div class="brand-sub">Sistema de Gestión para Grupos de Ahorro y Préstamo Comunitarios</div>', unsafe_allow_html=True)

        # Si NO hay sesión: mostrar login + registro (registro debajo)
        if not st.session_state.get("user"):
            st.markdown('<div class="login-title">Iniciar sesión</div>', unsafe_allow_html=True)
            st.markdown('<div class="muted">Accede con tu usuario y contraseña.</div>', unsafe_allow_html=True)

            # Login form
            with st.form("login_form"):
                usuario = st.text_input("Usuario", placeholder="usuario.ejemplo", label_visibility="collapsed")
                clave = st.text_input("Contraseña", type="password", placeholder="Contraseña", label_visibility="collapsed")
                c1, c2 = st.columns([1, 0.35])
                with c1:
                    entrar = st.form_submit_button("Entrar")
                with c2:
                    st.markdown('<button class="btn-ghost" type="button">¿Olvidaste?</button>', unsafe_allow_html=True)

                if entrar:
                    if not usuario or not clave:
                        st.error("Completa usuario y contraseña.")
                    else:
                        u = get_user_by_username(usuario)
                        if not u:
                            st.error("Usuario no encontrado.")
                        else:
                            if check_password_hash(u["password_hash"], clave):
                                # guardar datos de sesión
                                st.session_state.user = {
                                    "id": u["id"],
                                    "username": u["username"],
                                    "name": u.get("full_name"),
                                    "role": u.get("role"),
                                }
                                st.success(f"Bienvenido {u.get('full_name') or u['username']}!")
                                st.rerun()
                            else:
                                st.error("Contraseña incorrecta.")

            # espacio
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

            # Registro debajo del login
            st.markdown('<div style="margin-top:6px;"><b>Registrar usuario</b></div>', unsafe_allow_html=True)
            st.markdown('<div class="muted">Acceso limitado. Solo para administradores.</div>', unsafe_allow_html=True)

            with st.form("register_form"):
                ru = st.text_input("Usuario (nuevo)", placeholder="nuevo.usuario", label_visibility="collapsed")
                rn = st.text_input("Nombre completo", placeholder="Nombre Apellido", label_visibility="collapsed")
                rp = st.text_input("Contraseña", type="password", placeholder="Crear contraseña", label_visibility="collapsed")
                rp2 = st.text_input("Confirmar contraseña", type="password", placeholder="Confirmar contraseña", label_visibility="collapsed")
                rcol1, rcol2 = st.columns([1, 0.3])
                with rcol1:
                    reg_btn = st.form_submit_button("Registrar")
                with rcol2:
                    st.markdown('<button class="btn-ghost">Ayuda</button>', unsafe_allow_html=True)

                if reg_btn:
                    if not ru or not rp:
                        st.error("Usuario y contraseña obligatorios.")
                    elif rp != rp2:
                        st.error("Las contraseñas no coinciden.")
                    elif get_user_by_username(ru):
                        st.error("Usuario ya existe.")
                    else:
                        ok = register_user(ru, rp, rn)
                        if ok:
                            st.success("Usuario registrado correctamente. Inicia sesión.")
                        else:
                            st.error("No se pudo registrar el usuario (revisar logs).")

            # Mostrar movimientos también en vista pública (por si quieres que vean la actividad)
            st.markdown("<hr>", unsafe_allow_html=True)
            st.subheader("Movimientos recientes")
            movs = fetch_recent_movements(limit=6)
            rows = [{"Fecha": m.get("fecha",""), "Tipo": m.get("tipo",""), "Monto": m.get("monto",""), "Detalle": m.get("detalle","")} for m in movs]
            st.table(rows)

        # Si HAY sesión: ocultamos login y registro y mostramos DASHBOARD completo
        else:
            st.markdown(f"### Bienvenido, {st.session_state.user.get('name') or st.session_state.user.get('username')}")
            st.markdown("Acceso: **usuario autenticado** — aquí está el panel principal.")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            # Zona superior: Movimientos destacados (ocupa donde estaba el logo en diseños anteriores)
            st.subheader("Movimientos recientes")
            movs = fetch_recent_movements(limit=8)
            rows = [{"Fecha": m.get("fecha",""), "Tipo": m.get("tipo",""), "Monto": m.get("monto",""), "Detalle": m.get("detalle","")} for m in movs]
            st.table(rows)

            st.markdown("---")
            st.header("Dashboard — Resumen operativo")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Total miembros", value="—")
                st.write("Ahorros totales: —")
            with c2:
                st.metric("Préstamos vigentes", value="—")
                st.write("Mora (%): —")
            with c3:
                st.metric("Saldo caja", value="—")
                st.write("Próximos cierres: —")

            st.markdown("---")
            st.subheader("Actividad reciente")
            st.table([{"evento": "Pago", "miembro": "Juan", "monto": "$20"}, {"evento": "Aporte", "miembro": "Ana", "monto": "$5"}])

    # ------------------ RIGHT: ayuda reducida (sin panel DB) ------------------
    with right_col:
        st.markdown('<div class="side-card">', unsafe_allow_html=True)
        st.markdown('<div style="font-weight:600;margin-bottom:6px;">Documentación</div>', unsafe_allow_html=True)
        st.markdown(f'<a href="{logo_path}" target="_blank">Ver ER / Documentación</a>', unsafe_allow_html=True)
        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:13px;color:#A7B9DA">Contacto: admin@ejemplo.com</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close card
    st.markdown('</div>', unsafe_allow_html=True)  # close wrap

# --------------------------
# Sidebar / post-login controls
# --------------------------
if st.session_state.get("user"):
    st.sidebar.write(f"Conectado: **{st.session_state.user['username']}**")
    if st.sidebar.button("Cerrar sesión"):
        logout()
        st.rerun()

    menu = st.sidebar.radio("Navegación", ["Dashboard", "Guía visual", "Miembros", "Aportes", "Préstamos", "Reportes"])
    if menu == "Guía visual":
        render_guide_page()
    elif menu == "Dashboard":
        st.info("Estás en Dashboard (usa las tarjetas para mostrar métricas reales).")
    else:
        st.header(menu)
        st.write("Página en construcción.")

else:
    # si no hay sesión: detenemos ejecución después de mostrar login/reg (opcional)
    # st.stop()  # si lo activas, no carga sidebar; lo dejamos comentado para ver movimientos públicos
    pass

