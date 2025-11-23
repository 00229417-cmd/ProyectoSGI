# modulos/auth/auth.py
import os
from typing import Optional, Dict
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from modulos.config.conexion import get_engine

# --- SQL DDL (simple) ---
_CREATE_USERS_SQL = """
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(250),
    role VARCHAR(50) DEFAULT 'user',
    active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

def create_user_table_if_not_exists():
    """
    Crea la tabla de usuarios si no existe.
    """
    engine = get_engine()
    try:
        with engine.begin() as conn:
            conn.execute(text(_CREATE_USERS_SQL))
    except SQLAlchemyError as e:
        # solo logear / no crashar en producción
        print("create_user_table_if_not_exists error:", e)

def register_user(username: str, password: str, full_name: str = None, role: str = "user") -> bool:
    """
    Registra un usuario (con hash de contraseña). Retorna True si insertó correctamente.
    """
    engine = get_engine()
    password_hash = generate_password_hash(password)
    insert_sql = text(
        "INSERT INTO usuario (username, password_hash, full_name, role) VALUES (:username, :password_hash, :full_name, :role)"
    )
    try:
        with engine.begin() as conn:
            conn.execute(insert_sql, {"username": username, "password_hash": password_hash, "full_name": full_name, "role": role})
        return True
    except SQLAlchemyError as e:
        print("register_user error:", e)
        return False

def get_user_by_username(username: str) -> Optional[Dict]:
    """
    Devuelve un diccionario con los datos del usuario o None si no existe.
    IMPORTANTE: usa result.fetchone() para obtener la fila.
    """
    engine = get_engine()
    sel = text("SELECT id, username, password_hash, full_name, role, active FROM usuario WHERE username = :username LIMIT 1")
    try:
        with engine.connect() as conn:
            result = conn.execute(sel, {"username": username})
            row = result.fetchone()  # <-- aquí se obtiene la fila real
            if row:
                # row._mapping es compatible en SQLAlchemy 1.4+; convertimos a dict de manera segura
                try:
                    return dict(row._mapping)
                except Exception:
                    # fallback si no existe _mapping
                    return dict(row)
            else:
                return None
    except SQLAlchemyError as e:
        print("get_user_by_username error:", e)
        return None

# Helpers para sesión simple con Streamlit (si usas streamlit.session_state)
def init_session():
    try:
        import streamlit as st
        if "user" not in st.session_state:
            st.session_state["user"] = None
    except Exception:
        pass

def logout():
    try:
        import streamlit as st
        st.session_state.user = None
    except Exception:
        pass

