# modulos/db/crud_users.py
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from modulos.config.conexion import get_engine

# ---------- USERS (login) ----------
# Asume una tabla llamada `users` con columnas mínimas:
# id (PK autoinc), username (único), password_hash, full_name, role

def get_user_by_username(username: str):
    """Retorna dict con id, username, password_hash, full_name, role o None."""
    engine = get_engine()
    with engine.connect() as conn:
        q = text("""
            SELECT id, username, password_hash, full_name, role
            FROM users
            WHERE username = :u
            LIMIT 1
        """)
        row = conn.execute(q, {"u": username}).mappings().first()
        return dict(row) if row else None

def verify_user_credentials(username: str, password: str) -> bool:
    """Verifica credenciales; True si coinciden."""
    u = get_user_by_username(username)
    if not u:
        return False
    ph = u.get("password_hash")
    if not ph:
        return False
    return check_password_hash(ph, password)

def create_user(username: str, password: str, full_name: str = None, role: str = "user"):
    """
    Inserta usuario en tabla `users`. Devuelve lastrowid o True/False.
    No crea la tabla; asume que existe.
    """
    engine = get_engine()
    pw_hash = generate_password_hash(password)
    with engine.begin() as conn:
        q = text("""
            INSERT INTO users (username, password_hash, full_name, role)
            VALUES (:u, :ph, :fn, :r)
        """)
        res = conn.execute(q, {"u": username, "ph": pw_hash, "fn": full_name, "r": role})
        # res.lastrowid puede funcionar dependiendo del dialecto; si no, devolvemos True
        try:
            return res.lastrowid or True
        except Exception:
            return True

def update_user_password(username: str, new_password: str):
    """Actualiza el password_hash de un usuario."""
    engine = get_engine()
    new_hash = generate_password_hash(new_password)
    with engine.begin() as conn:
        q = text("UPDATE users SET password_hash = :ph WHERE username = :u")
        res = conn.execute(q, {"ph": new_hash, "u": username})
        return res.rowcount > 0

def list_users(limit: int = 100):
    """Lista usuarios (sin exponer password_hash cuando se consume en UI)."""
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id, username, full_name, role FROM users ORDER BY id DESC LIMIT :lim")
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]
