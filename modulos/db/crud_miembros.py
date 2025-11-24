# modulos/db/crud_miembros.py
from typing import List, Dict, Tuple, Optional
from sqlalchemy import text
from modulos.config.conexion import get_engine

def _fetchall_as_dicts(result_proxy) -> List[Dict]:
    rows = result_proxy.fetchall()
    keys = result_proxy.keys()
    return [dict(zip(keys, row)) for row in rows]

def list_miembros(limit: int = 500) -> Tuple[bool, List[Dict], Optional[str]]:
    """
    Devuelve (ok, rows, msg). rows es lista de dicts con columnas de la tabla `miembro`.
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            # Ajusta columnas si tu tabla tiene nombres diferentes; esta consulta asume la estructura mínima
            q = text("SELECT id_miembro, id_tipo_usuario, nombre, apellido, dui, direccion FROM miembro ORDER BY id_miembro DESC LIMIT :lim")
            res = conn.execute(q, {"lim": limit})
            rows = _fetchall_as_dicts(res)
        return True, rows, None
    except Exception as e:
        return False, [], str(e)

def create_miembro(nombre: str, apellido: str, dui: str = None, direccion: str = None, id_tipo_usuario: int = None) -> Tuple[bool, Optional[int], Optional[str]]:
    """
    Inserta un miembro y devuelve (ok, new_id, msg)
    """
    try:
        engine = get_engine()
        with engine.begin() as conn:
            q = text("""
                INSERT INTO miembro (id_tipo_usuario, nombre, apellido, dui, direccion)
                VALUES (:id_tipo_usuario, :nombre, :apellido, :dui, :direccion)
            """)
            res = conn.execute(q, {
                "id_tipo_usuario": id_tipo_usuario,
                "nombre": nombre,
                "apellido": apellido,
                "dui": dui,
                "direccion": direccion
            })
            # res.lastrowid puede variar; con SQLAlchemy 1.4 res.inserted_primary_key
            try:
                new_id = res.lastrowid
            except Exception:
                new_id = None
        return True, new_id, None
    except Exception as e:
        return False, None, str(e)




