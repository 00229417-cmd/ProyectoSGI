# modulos/db/crud_users.py
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from modulos.config.conexion import get_engine

def get_user_by_username(username: str):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id, username, password_hash, full_name, role FROM users WHERE username = :u LIMIT 1")
        r = conn.execute(q, {"u": username}).mappings().first()
        return dict(r) if r else None

def create_user(username: str, password: str, full_name: str = None, role: str = "user"):
    engine = get_engine()
    hashed = generate_password_hash(password)
    with engine.begin() as conn:
        q = text("INSERT INTO users (username, password_hash, full_name, role) VALUES (:u, :ph, :fn, :r)")
        res = conn.execute(q, {"u": username, "ph": hashed, "fn": full_name, "r": role})
        try:
            return res.lastrowid or True
        except Exception:
            return True

def list_users(limit=200):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id, username, full_name, role FROM users ORDER BY id DESC LIMIT :lim")
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

