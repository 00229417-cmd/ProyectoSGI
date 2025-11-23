# modulos/db/crud_users.py
from modulos.config.conexion import get_engine
from sqlalchemy import text
from werkzeug.security import generate_password_hash

def get_user_by_username(username):
    """
    Retorna dict con columnas si existe, sino None.
    Ajusta la consulta según el nombre real de la tabla en tu BD.
    """
    engine = get_engine()
    with engine.connect() as conn:
        # Ajusta 'users' por el nombre real (por ejemplo: usuario, Empleados, etc.)
        q = text("SELECT id, username, password_hash, full_name, role FROM users WHERE username = :u LIMIT 1")
        res = conn.execute(q, {"u": username}).mappings().first()
        return dict(res) if res else None

def create_user(username, password, full_name=None, role="user"):
    """
    Inserta un usuario en la tabla 'users'. No crea tabla.
    Devuelve inserted id (si tu BD autoinc devuelve) o True/False.
    """
    engine = get_engine()
    pw_hash = generate_password_hash(password)
    with engine.begin() as conn:
        q = text("INSERT INTO users (username, password_hash, full_name, role) VALUES (:u, :ph, :fn, :r)")
        res = conn.execute(q, {"u": username, "ph": pw_hash, "fn": full_name, "r": role})
        try:
            return res.lastrowid or True
        except Exception:
            return True

# Si necesitas crear también el 'miembro' en su tabla (si existe), adaptamos:
def create_member_for_user(user_id, nombre=None, telefono=None, direccion=None):
    engine = get_engine()
    with engine.begin() as conn:
        q = text("INSERT INTO miembro (id_usuario, nombre, telefono, direccion) VALUES (:uid, :n, :t, :d)")
        conn.execute(q, {"uid": user_id, "n": nombre, "t": telefono, "d": direccion})
        return True
