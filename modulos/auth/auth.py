# modulos/auth/auth.py
from typing import Optional, Dict
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from modulos.config.conexion import get_engine

CREATE_USERS_SQL = """
CREATE TABLE IF NOT EXISTS usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(250),
    role VARCHAR(50) DEFAULT 'user',
    active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

def create_user_table_if_not_exists():
    engine = get_engine()
    try:
        with engine.begin() as conn:
            conn.execute(text(CREATE_USERS_SQL))
    except SQLAlchemyError as e:
        print("create_user_table_if_not_exists error:", e)

def register_user(username: str, password: str, full_name: Optional[str]=None, role: str="user") -> bool:
    engine = get_engine()
    hashed = generate_password_hash(password)
    insert = text("INSERT INTO usuario (username, password_hash, full_name, role) VALUES (:username, :password_hash, :full_name, :role)")
    try:
        with engine.begin() as conn:
            conn.execute(insert, {"username":username, "password_hash":hashed, "full_name":full_name, "role":role})
        return True
    except SQLAlchemyError as e:
        print("register_user error:", e)
        return False

def get_user_by_username(username: str) -> Optional[Dict]:
    engine = get_engine()
    q = text("SELECT id, username, password_hash, full_name, role, active FROM usuario WHERE username = :username LIMIT 1")
    try:
        with engine.connect() as conn:
            r = conn.execute(q, {"username":username})
            row = r.fetchone()
            if row:
                try:
                    return dict(row._mapping)
                except Exception:
                    return dict(row)
            return None
    except SQLAlchemyError as e:
        print("get_user_by_username error:", e)
        return None

def init_session():
    try:
        import streamlit as st
        st.session_state.setdefault("session_iniciada", False)
        st.session_state.setdefault("usuario", None)
        st.session_state.setdefault("usuario_id", None)
    except Exception:
        pass

def logout():
    try:
        import streamlit as st
        st.session_state["session_iniciada"] = False
        st.session_state["usuario"] = None
        st.session_state["usuario_id"] = None
    except Exception:
        pass


