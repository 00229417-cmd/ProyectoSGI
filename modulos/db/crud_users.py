# modulos/db/crud_users.py
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from modulos.config.conexion import get_connection

# ---------- Lectura ----------
def get_user_by_username(username: str):
    """
    Devuelve: dict con columnas de la fila (id_user, username, password_hash, full_name, email, role, active, created_at)
    o None si no existe / en caso de error.
    """
    q = text("SELECT id_user, username, password_hash, full_name, email, role, active, created_at "
             "FROM users WHERE username = :u LIMIT 1")
    try:
        with get_connection() as conn:
            r = conn.execute(q, {"u": username})
            row = r.mappings().first()
            return dict(row) if row else None
    except SQLAlchemyError as e:
        # imprime en logs (Streamlit mostrará en consola); retorna None para no romper la app
        print("SQL ERROR get_user_by_username:", e)
        return None
    except Exception as e:
        print("Unexpected error get_user_by_username:", e)
        return None

# ---------- Creación ----------
def create_user(username: str, password: str, full_name: str = None, email: str = None, role: str = "user"):
    """
    Crea un usuario. Retorna id_user (si available) o True si success / False si falla (por ejemplo username duplicado).
    """
    hashed = generate_password_hash(password)
    q = text("INSERT INTO users (username, password_hash, full_name, email, role, active, created_at) "
             "VALUES (:u, :ph, :fn, :em, :r, 1, NOW())")
    try:
        with get_connection().begin() as conn:
            res = conn.execute(q, {"u": username, "ph": hashed, "fn": full_name, "em": email, "r": role})
            # mysql connector exposes lastrowid on result
            try:
                lastid = getattr(res, "lastrowid", None)
                return lastid if lastid else True
            except Exception:
                return True
    except SQLAlchemyError as e:
        print("SQL ERROR create_user:", e)
        return False
    except Exception as e:
        print("Unexpected error create_user:", e)
        return False

# ---------- Verificación de credenciales ----------
def verify_user_credentials(username: str, password: str):
    """
    Retorna: (True, user_dict) si ok; (False, None) si no; (False, "error mensaje") en caso de fallo técnico.
    """
    try:
        user = get_user_by_username(username)
        if not user:
            return False, None
        phash = user.get("password_hash")
        if not phash:
            return False, None
        ok = check_password_hash(phash, password)
        return (True, user) if ok else (False, None)
    except Exception as e:
        print("Unexpected error verify_user_credentials:", e)
        return False, str(e)

# ---------- Listado ----------
def list_users(limit: int = 200):
    q = text("SELECT id_user, username, full_name, email, role, active, created_at FROM users ORDER BY id_user DESC LIMIT :lim")
    try:
        with get_connection() as conn:
            rows = conn.execute(q, {"lim": limit}).mappings().all()
            return [dict(r) for r in rows]
    except SQLAlchemyError as e:
        print("SQL ERROR list_users:", e)
        return []
    except Exception as e:
        print("Unexpected error list_users:", e)
        return []

