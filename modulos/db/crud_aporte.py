# modulos/db/crud_miembros.py
from typing import List, Dict, Any, Optional
from sqlalchemy import text
from modulos.config.conexion import get_engine

def obtener_miembros(limit: int = 500) -> List[Dict[str, Any]]:
    """
    Devuelve la lista de miembros con las columnas existentes.
    """
    sql = text("""
        SELECT
            id_miembro,
            id_tipo_usuario,
            nombre,
            apellido,
            dui,
            direccion
        FROM miembro
        ORDER BY id_miembro DESC
        LIMIT :lim
    """)
    engine = get_engine()
    with engine.connect() as conn:
        res = conn.execute(sql, {"lim": limit})
        rows = res.mappings().all()
    return rows

def obtener_miembro_por_id(id_miembro: int) -> Optional[Dict[str, Any]]:
    sql = text("""
        SELECT
            id_miembro,
            id_tipo_usuario,
            nombre,
            apellido,
            dui,
            direccion
        FROM miembro
        WHERE id_miembro = :id_miembro
        LIMIT 1
    """)
    engine = get_engine()
    with engine.connect() as conn:
        res = conn.execute(sql, {"id_miembro": id_miembro})
        row = res.mappings().first()
    return row

def crear_miembro(data: Dict[str, Any]) -> int:
    """
    Crea un miembro. `data` debe contener keys:
      id_tipo_usuario, nombre, apellido, dui, direccion
    Retorna el id creado (si el engine lo soporta).
    """
    sql = text("""
        INSERT INTO miembro (
            id_tipo_usuario,
            nombre,
            apellido,
            dui,
            direccion
        ) VALUES (
            :id_tipo_usuario,
            :nombre,
            :apellido,
            :dui,
            :direccion
        )
    """)
    engine = get_engine()
    with engine.begin() as conn:
        res = conn.execute(sql, data)
        # intentar obtener lastrowid (depende del driver)
        try:
            return int(res.lastrowid)
        except Exception:
            return 0

def actualizar_miembro(id_miembro: int, data: Dict[str, Any]) -> bool:
    """
    Actualiza los campos permitidos de un miembro.
    data puede contener: id_tipo_usuario, nombre, apellido, dui, direccion
    """
    sql = text("""
        UPDATE miembro
        SET
            id_tipo_usuario = :id_tipo_usuario,
            nombre = :nombre,
            apellido = :apellido,
            dui = :dui,
            direccion = :direccion
        WHERE id_miembro = :id_miembro
    """)
    params = dict(data)
    params["id_miembro"] = id_miembro
    engine = get_engine()
    with engine.begin() as conn:
        res = conn.execute(sql, params)
        return res.rowcount > 0

def eliminar_miembro(id_miembro: int) -> bool:
    sql = text("DELETE FROM miembro WHERE id_miembro = :id_miembro")
    engine = get_engine()
    with engine.begin() as conn:
        res = conn.execute(sql, {"id_miembro": id_miembro})
        return res.rowcount > 0

# Opcional: obtener tipos de usuario si existe la tabla tipo_usuario
def obtener_tipos_usuario(limit: int = 200):
    sql = text("""
        SELECT id_tipo AS id_tipo_usuario, nombre
        FROM tipo_usuario
        ORDER BY id_tipo
        LIMIT :lim
    """)
    engine = get_engine()
    try:
        with engine.connect() as conn:
            res = conn.execute(sql, {"lim": limit})
            return res.mappings().all()
    except Exception:
        # si la tabla no existe o hay error, devolver lista vacía
        return []


