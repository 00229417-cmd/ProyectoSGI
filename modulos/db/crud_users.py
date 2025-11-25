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
from sqlalchemy import text
from modulos.config.conexion import get_engine
from werkzeug.security import generate_password_hash

def update_role(user_id: int, new_role: str) -> bool:
    """
    Actualiza exclusivamente el rol de un usuario.
    Retorna True si afectó al menos una fila, False en caso contrario.
    """
    try:
        uid = int(user_id)
    except Exception:
        return False

    engine = get_engine()
    try:
        with engine.begin() as conn:
            res = conn.execute(
                text("UPDATE users SET role = :role WHERE id = :id"),
                {"role": new_role, "id": uid},
            )
        return (res.rowcount if hasattr(res, "rowcount") else 0) > 0
    except Exception:
        return False


def update_user(user_id: int, data: dict | None = None, *args) -> bool:
    """
    Actualiza campos de un usuario. Dos formas de uso:
      - update_user(id, {"full_name": "...", "email": "...", "role": "...", "password": "..."})
      - update_user(id, full_name, email)  <- fallback posicional (solo nombre y correo)

    Campos permitidos en `data`: full_name, email, role, password, username (si lo permites).
    Si se incluye 'password', se hashéa antes de guardar.

    Retorna True si se actualizó (rowcount>0), False en caso contrario.
    """
    try:
        uid = int(user_id)
    except Exception:
        return False

    # fallback posicional: (full_name, email)
    if data is None and args:
        data = {}
        if len(args) >= 1:
            data["full_name"] = args[0]
        if len(args) >= 2:
            data["email"] = args[1]

    if not data or not isinstance(data, dict):
        return False

    # filtrar solo campos permitidos
    allowed = {"full_name", "email", "role", "password", "username"}
    updates = {}
    for k, v in data.items():
        if k in allowed and v is not None:
            updates[k] = v

    if not updates:
        return False

    # si actualizan password, hashéala
    if "password" in updates:
        try:
            updates["password_hash"] = generate_password_hash(updates.pop("password"))
            # si tu tabla usa otra columna para hash, ajusta aquí
        except Exception:
            return False

    # construir SET dinámico y parámetros
    set_parts = []
    params = {"id": uid}
    col_map = {
        "full_name": "full_name",
        "email": "email",
        "role": "role",
        "username": "username",
        "password_hash": "password_hash",
    }

    for i, (k, v) in enumerate(updates.items()):
        col = col_map.get(k, k)
        param_name = f"p{i}"
        set_parts.append(f"{col} = :{param_name}")
        params[param_name] = v

    set_clause = ", ".join(set_parts)
    sql = text(f"UPDATE users SET {set_clause} WHERE id = :id")

    engine = get_engine()
    try:
        with engine.begin() as conn:
            res = conn.execute(sql, params)
        return (res.rowcount if hasattr(res, "rowcount") else 0) > 0
    except Exception:
        return False


