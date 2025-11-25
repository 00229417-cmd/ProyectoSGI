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
            conn.execute(q, {"u": username, "ph": hashed, "fn": full_name, "em": email, "r": role})
            return True
        except Exception:
            return False

def verify_user_credentials(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return False, "Usuario no encontrado."
    ph = user.get("password_hash")
    try:
        if check_password_hash(ph, password):
            return True, user
        else:
            return False, "Contraseña incorrecta."
    except Exception:
        return False, "Error al verificar credenciales."

def list_users(limit: int = 200):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id, username, full_name, email, role, created_at FROM users ORDER BY id DESC LIMIT :lim")
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def change_password(user_id: int, current: str, new: str) -> bool:
    """
    Cambia la contraseña de un usuario:
      - Verifica que el usuario exista.
      - Comprueba que `current` coincide con la hash actual.
      - Si OK, actualiza la hash por la de `new`.

    Retorna True si el cambio se realizó correctamente, False en caso contrario.
    """
    engine = get_engine()
    try:
        # 1) obtener hash actual
        with engine.connect() as conn:
            r = conn.execute(
                text("SELECT password_hash FROM users WHERE id = :id LIMIT 1"),
                {"id": user_id}
            ).mappings().first()

        if not r:
            return False  # usuario no existe

        current_hash = r.get("password_hash")
        if not current_hash:
            return False

        # 2) verificar contraseña actual
        if not check_password_hash(current_hash, current):
            return False  # contraseña actual incorrecta

        # 3) generar nueva hash y actualizar
        new_hash = generate_password_hash(new)
        with engine.begin() as conn:
            conn.execute(
                text("UPDATE users SET password_hash = :ph WHERE id = :id"),
                {"ph": new_hash, "id": user_id}
            )

        return True
    except Exception:
        # En producción querrás loggear el error; aquí devolvemos False para mantener la API simple
        return False


