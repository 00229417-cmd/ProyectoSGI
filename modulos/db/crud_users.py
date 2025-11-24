# modulos/db/crud_users.py
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from modulos.config.conexion import get_engine

def get_user_by_username(username: str):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id, username, password_hash, full_name, email, role FROM users WHERE username = :u LIMIT 1")
        r = conn.execute(q, {"u": username}).mappings().first()
        return dict(r) if r else None

def create_user(username: str, password: str, full_name: str = None, email: str = None, role: str = "user"):
    engine = get_engine()
    hashed = generate_password_hash(password)
    with engine.begin() as conn:
        q = text("""
            INSERT INTO users (username, password_hash, full_name, email, role)
            VALUES (:u, :ph, :fn, :em, :r)
        """)
        try:
            res = conn.execute(q, {"u": username, "ph": hashed, "fn": full_name, "em": email, "r": role})
            # retornamos True si OK
            return True
        except Exception:
            return False

def verify_user_credentials(username: str, password: str):
    """
    devuelve (True, user_dict) si OK, (False, mensaje) si error
    """
    user = get_user_by_username(username)
    if not user:
        return False, "Usuario no encontrado."
    ph = user.get("password_hash")
    try:
        if check_password_hash(ph, password):
            return True, user
        else:
            return False, "Contraseña incorrecta."
    except Exception as e:
        return False, "Error al verificar credenciales."

