import streamlit as st
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from modulos.config.conexion import get_engine

def create_user_table_if_not_exists():
    engine = get_engine()
    sql = """
    CREATE TABLE IF NOT EXISTS usuario_auth (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(120) UNIQUE,
        password_hash VARCHAR(255),
        full_name VARCHAR(150),
        role VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    with engine.begin() as conn:
        conn.execute(text(sql))

def register_user(username: str, password: str, full_name: str = "", role: str = "member"):
    engine = get_engine()
    pw_hash = generate_password_hash(password)
    sql = text("INSERT INTO usuario_auth (username, password_hash, full_name, role) VALUES (:u, :p, :f, :r)")
    with engine.begin() as conn:
        conn.execute(sql, {"u": username, "p": pw_hash, "f": full_name, "r": role})

def get_user_by_username(username: str):
    engine = get_engine()
    sql = text("SELECT id, username, password_hash, full_name, role FROM usuario_auth WHERE username = :u")
    with engine.connect() as conn:
        r = conn.execute(sql, {"u": username}).fetchone()
        return dict(r) if r else None

def init_session():
    if "user" not in st.session_state:
        st.session_state.user = None

def login_form():
    init_session()
    st.subheader("Iniciar sesión")
    username = st.text_input("Usuario", key="login_user")
    password = st.text_input("Contraseña", type="password", key="login_pw")
    if st.button("Entrar", key="login_btn"):
        user = get_user_by_username(username)
        if not user:
            st.error("Usuario no encontrado.")
            return False
        if check_password_hash(user["password_hash"], password):
            st.session_state.user = {
                "id": user["id"],
                "username": user["username"],
                "name": user["full_name"],
                "role": user["role"],
            }
            st.success(f"¡Bienvenido {user['full_name'] or user['username']}!")
            return True
        else:
            st.error("Contraseña incorrecta.")
            return False
    return False

def logout():
    st.session_state.user = None
    st.success("Has cerrado sesión.")

def register_form():
    st.subheader("Registrar nuevo usuario")
    username = st.text_input("Usuario (nuevo)", key="reg_user")
    full_name = st.text_input("Nombre completo", key="reg_name")
    password = st.text_input("Contraseña", type="password", key="reg_pw")
    password2 = st.text_input("Confirmar contraseña", type="password", key="reg_pw2")
    if st.button("Registrar", key="reg_btn"):
        if not username or not password:
            st.error("Usuario y contraseña son obligatorios.")
            return
        if password != password2:
            st.error("Las contraseñas no coinciden.")
            return
        if get_user_by_username(username):
            st.error("Usuario ya existe.")
            return
        register_user(username, password, full_name)
        st.success("Usuario registrado. Inicia sesión.")
