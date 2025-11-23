
# modulos/db/crud_miembro.py
"""
CRUD para la tabla `miembro`.

Funciones incluidas:
- create_member(...)
- get_member_by_id(id)
- get_member_by_dui(dui)
- list_members(limit=100, offset=0, search=None)
- update_member(member_id, **fields)
- soft_delete_member(member_id)   -> marca estado = 'inactivo'
- hard_delete_member(member_id)   -> elimina fila (USE CON PRECAUCIÓN)
"""

from typing import Optional, List, Dict, Any
import logging
from sqlalchemy import text
from modulos.config.conexion import get_engine

logger = logging.getLogger(__name__)


def _row_to_dict(row) -> Dict[str, Any]:
    """Convierte una RowMapping a dict o devuelve None si row es None."""
    return dict(row) if row is not None else None


def create_member(
    id_tipo_usuario: Optional[int] = None,
    nombre: Optional[str] = None,
    apellido: Optional[str] = None,
    dui: Optional[str] = None,
    direccion: Optional[str] = None,
    telefono: Optional[str] = None,
    email: Optional[str] = None,
    id_grupo: Optional[int] = None,
    estado: str = "activo",
) -> Optional[int]:
    """
    Inserta un nuevo miembro. Devuelve el id creado (int) o None en error.
    Los nombres de columnas deben coincidir con tu tabla `miembro`.
    """
    engine = get_engine()
    sql = text(
        """
        INSERT INTO miembro
            (id_tipo_usuario, nombre, apellido, dui, direccion, telefono, email, id_grupo, estado)
        VALUES
            (:id_tipo_usuario, :nombre, :apellido, :dui, :direccion, :telefono, :email, :id_grupo, :estado)
        """
    )
    params = {
        "id_tipo_usuario": id_tipo_usuario,
        "nombre": nombre,
        "apellido": apellido,
        "dui": dui,
        "direccion": direccion,
        "telefono": telefono,
        "email": email,
        "id_grupo": id_grupo,
        "estado": estado,
    }

    try:
        with engine.begin() as conn:
            res = conn.execute(sql, params)
            # En MySQL, obtener id insertado con SELECT LAST_INSERT_ID()
            r = conn.execute(text("SELECT LAST_INSERT_ID() AS id")).mappings().first()
            return int(r["id"]) if r and r.get("id") is not None else None
    except Exception as e:
        logger.exception("Error creando miembro: %s", e)
        return None


def get_member_by_id(member_id: int) -> Optional[Dict[str, Any]]:
    """Devuelve un dict con los datos del miembro o None si no existe."""
    engine = get_engine()
    sql = text("SELECT * FROM miembro WHERE id_miembro = :id LIMIT 1")
    try:
        with engine.connect() as conn:
            r = conn.execute(sql, {"id": member_id}).mappings().first()
            return _row_to_dict(r)
    except Exception as e:
        logger.exception("Error get_member_by_id: %s", e)
        return None


def get_member_by_dui(dui: str) -> Optional[Dict[str, Any]]:
    """Buscar miembro por DUI (único)."""
    engine = get_engine()
    sql = text("SELECT * FROM miembro WHERE dui = :dui LIMIT 1")
    try:
        with engine.connect() as conn:
            r = conn.execute(sql, {"dui": dui}).mappings().first()
            return _row_to_dict(r)
    except Exception as e:
        logger.exception("Error get_member_by_dui: %s", e)
        return None


def list_members(limit: int = 100, offset: int = 0, search: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Lista miembros con paginación.
    Si `search` está presente, hace búsqueda simple en nombre/apellido/dui.
    """
    engine = get_engine()
    try:
        with engine.connect() as conn:
            if search:
                q = text(
                    """
                    SELECT * FROM miembro
                    WHERE nombre LIKE :s OR apellido LIKE :s OR dui LIKE :s
                    ORDER BY id_miembro DESC
                    LIMIT :lim OFFSET :off
                    """
                )
                param = {"s": f"%{search}%", "lim": limit, "off": offset}
                rows = conn.execute(q, param).mappings().all()
            else:
                q = text(
                    """
                    SELECT * FROM miembro
                    ORDER BY id_miembro DESC
                    LIMIT :lim OFFSET :off
                    """
                )
                rows = conn.execute(q, {"lim": limit, "off": offset}).mappings().all()
            return [dict(r) for r in rows]
    except Exception as e:
        logger.exception("Error list_members: %s", e)
        return []


def update_member(member_id: int, **fields) -> bool:
    """
    Actualiza los campos proporcionados para el miembro.
    Uso: update_member(3, nombre='Juan', direccion='Nueva')
    Devuelve True si se actualizó al menos una fila.
    """
    if not fields:
        return False

    # Validar keys válidas (evitar inyección de columnas)
    valid_cols = {
        "id_tipo_usuario",
        "nombre",
        "apellido",
        "dui",
        "direccion",
        "telefono",
        "email",
        "id_grupo",
        "estado",
    }
    set_parts = []
    params = {}
    for k, v in fields.items():
        if k in valid_cols:
            set_parts.append(f"{k} = :{k}")
            params[k] = v
    if not set_parts:
        return False

    params["id_miembro"] = member_id
    sql = text(f"UPDATE miembro SET {', '.join(set_parts)} WHERE id_miembro = :id_miembro")
    engine = get_engine()
    try:
        with engine.begin() as conn:
            res = conn.execute(sql, params)
            return (res.rowcount if hasattr(res, "rowcount") else 0) > 0
    except Exception as e:
        logger.exception("Error update_member: %s", e)
        return False


def soft_delete_member(member_id: int) -> bool:
    """Marca el miembro como inactivo (estado='inactivo')."""
    return update_member(member_id, estado="inactivo")


def hard_delete_member(member_id: int) -> bool:
    """Elimina físicamente el miembro (usar con precaución)."""
    engine = get_engine()
    sql = text("DELETE FROM miembro WHERE id_miembro = :id")
    try:
        with engine.begin() as conn:
            res = conn.execute(sql, {"id": member_id})
            return (res.rowcount if hasattr(res, "rowcount") else 0) > 0
    except Exception as e:
        logger.exception("Error hard_delete_member: %s", e)
        return False
