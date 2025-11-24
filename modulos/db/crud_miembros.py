# modulos/db/crud_miembros.py
from sqlalchemy import text
from typing import List, Optional
from modulos.config.conexion import get_engine

def list_miembros(limit: int = 500) -> List[dict]:
    engine = get_engine()
    q = text("""
        SELECT id_miembro, id_tipo_usuario, nombre, apellido, dui, direccion
        FROM miembro
        ORDER BY id_miembro DESC
        LIMIT :lim
    """)
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def get_miembro_by_id(id_miembro: int) -> Optional[dict]:
    engine = get_engine()
    q = text("SELECT id_miembro, id_tipo_usuario, nombre, apellido, dui, direccion FROM miembro WHERE id_miembro = :id LIMIT 1")
    with engine.connect() as conn:
        r = conn.execute(q, {"id": id_miembro}).mappings().first()
        return dict(r) if r else None

def create_miembro(nombre: str, apellido: str, id_tipo_usuario: int = None, dui: str = None, direccion: str = None):
    engine = get_engine()
    q = text("""
        INSERT INTO miembro (id_tipo_usuario, nombre, apellido, dui, direccion)
        VALUES (:tipo, :nom, :ape, :dui, :dir)
    """)
    with engine.begin() as conn:
        res = conn.execute(q, {"tipo": id_tipo_usuario, "nom": nombre, "ape": apellido, "dui": dui, "dir": direccion})
        # res.lastrowid works en algunos DBAPIs; devolvemos True si no falla
        try:
            return res.lastrowid or True
        except Exception:
            return True

def update_miembro(id_miembro: int, nombre: str, apellido: str, id_tipo_usuario: int = None, dui: str = None, direccion: str = None):
    engine = get_engine()
    q = text("""
        UPDATE miembro SET id_tipo_usuario = :tipo, nombre = :nom, apellido = :ape, dui = :dui, direccion = :dir
        WHERE id_miembro = :id
    """)
    with engine.begin() as conn:
        conn.execute(q, {"tipo": id_tipo_usuario, "nom": nombre, "ape": apellido, "dui": dui, "dir": direccion, "id": id_miembro})
        return True

def delete_miembro(id_miembro: int):
    engine = get_engine()
    q = text("DELETE FROM miembro WHERE id_miembro = :id")
    with engine.begin() as conn:
        conn.execute(q, {"id": id_miembro})
        return True


