# modulos/db/crud_miembros.py
"""
CRUD REAL para la tabla 'miembro'

Columnas vistas en tu phpMyAdmin:
id_miembro, id_tipo_usuario, nombre, apellido, dui, direccion
"""

from sqlalchemy import text
from modulos.config.conexion import get_engine


# ----------------------------------------
# LISTAR MIEMBROS
# ----------------------------------------
def list_members(limit: int = 200):
    """
    Devuelve una lista de miembros.
    """
    engine = get_engine()
    with engine.connect() as conn:
        q = text("""
            SELECT 
                id_miembro AS id,
                nombre,
                apellido,
                dui,
                direccion,
                id_tipo_usuario
            FROM miembro
            ORDER BY id_miembro DESC
            LIMIT :lim
        """)
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]


# ----------------------------------------
# CREAR MIEMBRO
# ----------------------------------------
def create_member(nombre: str, apellido: str, dui: str, direccion: str, tipo_usuario: int):
    engine = get_engine()
    with engine.begin() as conn:
        q = text("""
            INSERT INTO miembro (nombre, apellido, dui, direccion, id_tipo_usuario)
            VALUES (:n, :a, :d, :dir, :t)
        """)
        try:
            conn.execute(q, {
                "n": nombre,
                "a": apellido,
                "d": dui,
                "dir": direccion,
                "t": tipo_usuario
            })
            return True
        except Exception as e:
            print("ERROR create_member:", e)
            return False


# ----------------------------------------
# OBTENER MIEMBRO POR ID
# ----------------------------------------
def get_member_by_id(member_id: int):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("""
            SELECT 
                id_miembro AS id,
                nombre,
                apellido,
                dui,
                direccion,
                id_tipo_usuario
            FROM miembro
            WHERE id_miembro = :id
            LIMIT 1
        """)
        row = conn.execute(q, {"id": member_id}).mappings().first()
        return dict(row) if row else None


# ----------------------------------------
# ACTUALIZAR MIEMBRO
# ----------------------------------------
def update_member(member_id: int, nombre: str, apellido: str, dui: str, direccion: str, tipo_usuario: int):
    engine = get_engine()
    with engine.begin() as conn:
        q = text("""
            UPDATE miembro
            SET nombre = :n,
                apellido = :a,
                dui = :d,
                direccion = :dir,
                id_tipo_usuario = :t
            WHERE id_miembro = :id
        """)
        try:
            conn.execute(q, {
                "n": nombre,
                "a": apellido,
                "d": dui,
                "dir": direccion,
                "t": tipo_usuario,
                "id": member_id
            })
            return True
        except Exception as e:
            print("ERROR update_member:", e)
            return False


# ----------------------------------------
# ELIMINAR MIEMBRO
# ----------------------------------------
def delete_member(member_id: int):
    engine = get_engine()
    with engine.begin() as conn:
        q = text("DELETE FROM miembro WHERE id_miembro = :id")
        try:
            conn.execute(q, {"id": member_id})
            return True
        except Exception as e:
            print("ERROR delete_member:", e)
            return False


