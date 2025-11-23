# modulos/login.py
import streamlit as st
from werkzeug.security import check_password_hash

# imports internos (si faltan se manejan errores mostrando mensajes)
try:
    from modulos.auth.auth import (
        create_user_table_if_not_exists,
        init_session,
        get_user_by_username,
    )
except Exception:
    # fallback: definiciones mínimas para evitar crashes si el módulo falta
    def create_user_table_if_not_exists():
        pass

    def init_session():
        pass

    def get_user_by_username(username):
        return None

try:
    from modulos.db.crud_users import create_user_and_member
except Exception:
    # fallback: función que muestra error si no existe el CRUD
    def create_user_and_member(*args, **kwargs):
        st.error("Funcionalidad create_user_and_member no disponible. Crea modulos/db/crud_users.py")
        return None

# Aseguramos tabla/estado
create_user_table_if_not_exists()
init_session()

# ----------------------------------------
# Ruta local del ER (workspace):
ER_LOCAL_URL = "file:///mnt/data/ER proyecto - ER NUEVO.png"
# Si prefieres usar raw GitHub, reemplaza ER_LOCAL_URL por la URL raw de GitHub.
ER_URL = ER_LOCAL_URL
# ----------------------------------------

def login_page():
    """
    Página de login con estilo 'premium' y registro interactivo.
    - Registro crea usuario + miembro (create_user_and_member).
    - Botón discreto bottom-right abre la documentación/ER.
    """

    # CSS y animaciones sutiles
    st.markdown(
        """
        <style>
        header { visibility: hidden; }
        main { padding-top: 0rem; }

        .login-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
            border-radius:12px; padding:18px; box-shadow:0 12px 30px rgba(0,0,0,0.45);
            animation: fadeInUp 0.6s ease-out both;
        }
        @keyframes fadeInUp { 0% { opacity: 0; transform: translateY(12px); } 100% { opacity: 1; transform: translateY(0); } }

        .logo-small {
          width:76px; height:76px; border-radius:14px;
          background: linear-gradient(135deg,#5b8bff,#3c67d6);
          display:flex; align-items:center; justify-content:center;
          color:white; font-weight:800; font-size:28px;
          box-shadow: 0 10px 36px rgba(20,40,120,0.28);
          animation: floaty 6s ease-in-out infinite;
        }
        @keyframes floaty { 0% { transform: translateY(0px); } 50% { transform: translateY(-6px); } 100% { transform: translateY(0px); } }

        .brand-title { font-size:28px; margin:0; color:#F7FBFF; }
        .brand-sub { font-size:13px; color:#9FB4D6; margin-top:6px; }

        .login-title { font-size:18px; color:#EAF2FF; margin-top:6px; }
        .muted { color:#9FB4D6; font-size:13px; margin-bottom:8px; }

        .er-button {
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
        }
        .er-button svg { width:20px; height:20px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col_main, col_right = st.columns([1.8, 0.9])

    with col_main:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        brand_cols = st.columns([0.14, 1])
        with brand_cols[0]:
            st.markdown('<div class="logo-small">G</div>', unsafe_allow_html=True)
        with brand_cols[1]:
            st.markdown('<div class="brand-title">GAPC — Portal</div>', unsafe_allow_html=True)
            st.markdown('<div class="brand-sub">Sistema de Gestión para Grupos de Ahorro y Préstamo Comunitarios</div>', unsafe_allow_html=True)

        st.markdown('<div class="login-title">Iniciar sesión</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted">Accede con tu usuario y contraseña.</div>', unsafe_allow_html=True)

        with st.form(key="form_login", clear_on_submit=False):
            username = st.text_input("Usuario", placeholder="usuario.ejemplo", label_visibility="collapsed")
            password = st.text_input("Contraseña", type="password", placeholder="Contraseña", label_visibility="collapsed")

            c1, c2 = st.columns([0.6, 0.4])
            with c1:
                btn_login = st.form_submit_button("Entrar")
            with c2:
                if st.form_submit_button("Registrar usuario", use_container_width=True, key="open_register_btn"):
                    st.session_state.setdefault("mostrar_registro", True)

            if btn_login:
                if not username or not password:
                    st.error("Completa usuario y contraseña.")
                else:
                    u = get_user_by_username(username)
                    if not u:
                        st.error("Usuario no encontrado.")
                    else:
                        password_hash = u.get("password_hash") if isinstance(u, dict) else getattr(u, "password_hash", None)
                        if password_hash and check_password_hash(password_hash, password):
                            st.session_state["session_iniciada"] = True
                            st.session_state["usuario"] = username
                            try:
                                st.session_state["usuario_id"] = u.get("id") if isinstance(u, dict) else getattr(u, "id", None)
                            except Exception:
                                pass
                            try:
                                st.session_state["user_role"] = u.get("role") if isinstance(u, dict) else getattr(u, "role", None)
                            except Exception:
                                pass
                            st.success(f"Bienvenido {u.get('full_name') or username if isinstance(u, dict) else username}!")
                            try:
                                st.rerun()
                            except Exception:
                                st.experimental_rerun()
                        else:
                            st.error("Contraseña incorrecta.")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        show_reg = st.session_state.get("mostrar_registro", False)
        exp = st.expander("Registrar usuario" if not show_reg else "Registrar usuario (ocultar)", expanded=show_reg)
        with exp:
            with st.form(key="form_register"):
                r_user = st.text_input("Usuario (nuevo)", placeholder="nuevo.usuario", label_visibility="collapsed")
                r_name = st.text_input("Nombre completo", placeholder="Nombre Apellido", label_visibility="collapsed")
                r_dni = st.text_input("Identificación (opcional)", placeholder="DUI/ID", label_visibility="collapsed")
                r_tel = st.text_input("Teléfono (opcional)", placeholder="Teléfono", label_visibility="collapsed")
                r_dir = st.text_input("Dirección (opcional)", placeholder="Dirección", label_visibility="collapsed")
                r_pwd = st.text_input("Contraseña", type="password", placeholder="Crear contraseña", label_visibility="collapsed")
                r_pwd2 = st.text_input("Confirmar contraseña", type="password", placeholder="Confirmar contraseña", label_visibility="collapsed")

                rcol1, rcol2 = st.columns([0.7, 0.3])
                with rcol1:
                    btn_reg = st.form_submit_button("Registrar")
                with rcol2:
                    if st.form_submit_button("Cancelar", key="cancel_reg"):
                        st.session_state["mostrar_registro"] = False

                if btn_reg:
                    if not r_user or not r_pwd:
                        st.error("Usuario y contraseña obligatorios.")
                    elif r_pwd != r_pwd2:
                        st.error("Las contraseñas no coinciden.")
                    elif get_user_by_username(r_user):
                        st.error("Usuario ya existe.")
                    else:
                        user_id = create_user_and_member(
                            username=r_user,
                            password=r_pwd,
                            full_name=r_name,
                            dni=r_dni,
                            telefono=r_tel,
                            direccion=r_dir,
                            role="user"
                        )
                        if user_id:
                            st.success("Usuario y miembro creados correctamente. Inicia sesión.")
                            st.session_state["mostrar_registro"] = False
                        else:
                            st.error("No se pudo crear el usuario. Revisa logs.")

        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    er_html = f'''
    <a href="{ER_URL}" target="_blank" class="er-button" title="Documentación (ER)">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M7 2H13L18 7V22H7V2Z" fill="white" fill-opacity="0.95"/>
            <path d="M13 2V7H18" stroke="white" stroke-opacity="0.6" stroke-width="0.6"/>
        </svg>
    </a>
    '''
    st.markdown(er_html, unsafe_allow_html=True)

if __name__ == "__main__":
    try:
        login_page()
    except Exception as e:
        print("Error al ejecutar login_page (debug):", e)

