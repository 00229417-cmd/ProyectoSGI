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

def create_user(username: str, password: str, full_name: str = None, email: str = None, role: str = "user"):
    """
    Inserta usuario. Devuelve True si OK, False o texto de error si falla.
    """
    engine = get_engine()
    hashed = generate_password_hash(password)
    try:
        with engine.begin() as conn:
            q = text("""
                INSERT INTO users (username, password_hash, full_name, email, role)
                VALUES (:u, :ph, :fn, :em, :r)
            """)
            res = conn.execute(q, {"u": username, "ph": hashed, "fn": full_name, "em": email, "r": role})
            # res.rowcount generalmente = 1
        return True
    except Exception as e:
        # devuelve el mensaje para debugging (puedes registrar en logs)
        return False

def verify_user_credentials(username: str, password: str):
    """
    Verifica credenciales. Devuelve (True, user_dict) si OK, (False, mensaje) si no.
    """
    u = get_user_by_username(username)
    if not u:
        return False, "usuario no existe"
    ph = u.get("password_hash")
    if not ph:
        return False, "hash no encontrado"
    if check_password_hash(ph, password):
        return True, u
    return False, "contraseña inválida"


