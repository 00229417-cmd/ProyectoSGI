# modulos/db/crud_miembros.py
from typing import List, Dict, Tuple, Optional
from sqlalchemy import text
from modulos.config.conexion import get_engine

# Nota: no importes páginas u otros módulos que importen a este para evitar imports circulares.

def list_miembros(limit: int = 500) -> List[Dict]:
    """
    Retorna lista de miembros como diccionarios.
    """
    engine = get_engine()
    sql = text(
        "SELECT id_miembro, id_tipo_usuario, nombre, apellido, dui, direccion "
        "FROM miembro ORDER BY id_miembro DESC LIMIT :lim"
    )
    with engine.connect() as conn:
        result = conn.execute(sql, {"lim": limit})
        rows = [dict(r._mapping) for r in result.fetchall()]
    return rows


def get_miembro(id_miembro: int) -> Optional[Dict]:
    engine = get_engine()
    sql = text(
        "SELECT id_miembro, id_tipo_usuario, nombre, apellido, dui, direccion "
        "FROM miembro WHERE id_miembro = :id"
    )
    with engine.connect() as conn:
        r = conn.execute(sql, {"id": id_miembro}).fetchone()
        return dict(r._mapping) if r else None


def create_miembro(id_tipo_usuario: Optional[int], nombre: str, apellido: str, dui: str, direccion: str) -> Tuple[bool, str]:
    engine = get_engine()
    sql = text(
        "INSERT INTO miembro (id_tipo_usuario, nombre, apellido, dui, direccion) "
        "VALUES (:id_tipo_usuario, :nombre, :apellido, :dui, :direccion)"
    )
    try:
        with engine.begin() as conn:
            conn.execute(sql, {
                "id_tipo_usuario": id_tipo_usuario,
                "nombre": nombre,
                "apellido": apellido,
                "dui": dui,
                "direccion": direccion
            })
        return True, "Miembro creado correctamente."
    except Exception as e:
        return False, f"Error creando miembro: {e}"


def update_miembro(id_miembro: int, id_tipo_usuario: Optional[int], nombre: str, apellido: str, dui: str, direccion: str) -> Tuple[bool, str]:
    engine = get_engine()
    sql = text(
        "UPDATE miembro SET id_tipo_usuario = :id_tipo_usuario, nombre = :nombre, apellido = :apellido, "
        "dui = :dui, direccion = :direccion WHERE id_miembro = :id_miembro"
    )
    try:
        with engine.begin() as conn:
            conn.execute(sql, {
                "id_tipo_usuario": id_tipo_usuario,
                "nombre": nombre,
                "apellido": apellido,
                "dui": dui,
                "direccion": direccion,
                "id_miembro": id_miembro
            })
        return True, "Miembro actualizado."
    except Exception as e:
        return False, f"Error actualizando miembro: {e}"


def delete_miembro(id_miembro: int) -> Tuple[bool, str]:
    engine = get_engine()
    sql = text("DELETE FROM miembro WHERE id_miembro = :id")
    try:
        with engine.begin() as conn:
            conn.execute(sql, {"id": id_miembro})
        return True, "Miembro eliminado."
    except Exception as e:
        return False, f"Error eliminando miembro: {e}"



