# modulos/db/crud_miembros.py
from typing import Optional, List, Dict, Any
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from modulos.config.conexion import get_engine


def _row_to_dict(row) -> Dict[str, Any]:
    """Convierte row.mapping / row a dict, si es None devuelve None"""
    if not row:
        return None
    try:
        return dict(row)
    except Exception:
        # si no es RowMapping, intenta convertir por atributos
        return {k: getattr(row, k) for k in row.keys()}


# -------------------------
# Listar miembros (paginado simple)
# -------------------------
def list_members(limit: int = 200, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Devuelve una lista de miembros (limit, offset).
    """
    engine = get_engine()
    q = text(
        """
        SELECT id_miembro, id_tipo_usuario, nombre, apellido, dui, direccion
        FROM miembro
        ORDER BY id_miembro DESC
        LIMIT :lim OFFSET :off
        """
    )
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit, "off": offset}).mappings().all()
        return [dict(r) for r in rows]


# -------------------------
# Obtener miembro por id
# -------------------------
def get_member_by_id(member_id: int) -> Optional[Dict[str, Any]]:
    engine = get_engine()
    q = text(
        """
        SELECT id_miembro, id_tipo_usuario, nombre, apellido, dui, direccion
        FROM miembro
        WHERE id_miembro = :mid
        LIMIT 1
        """
    )
    with engine.connect() as conn:
        r = conn.execute(q, {"mid": member_id}).mappings().first()
        return dict(r) if r else None


# -------------------------
# Buscar miembros por nombre/apellido parcial
# -------------------------
def search_members(term: str, limit: int = 100) -> List[Dict[str, Any]]:
    engine = get_engine()
    like = f"%{term}%"
    q = text(
        """
        SELECT id_miembro, id_tipo_usuario, nombre, apellido, dui, direccion
        FROM miembro
        WHERE nombre LIKE :like OR apellido LIKE :like OR dui LIKE :like
        ORDER BY nombre, apellido
        LIMIT :lim
        """
    )
    with engine.connect() as conn:
        rows = conn.execute(q, {"like": like, "lim": limit}).mappings().all()
        return [dict(r) for r in rows]


# -------------------------
# Crear miembro
# -------------------------
def create_member(id_tipo_usuario: Optional[int],
                  nombre: str,
                  apellido: str,
                  dui: Optional[str] = None,
                  direccion: Optional[str] = None) -> Optional[int]:
    """
    Inserta un miembro; devuelve el id generado si se puede obtener (MySQL),
    o True si la inserción se completó y el driver no provee lastrowid.
    """
    engine = get_engine()
    q = text(
        """
        INSERT INTO miembro (id_tipo_usuario, nombre, apellido, dui, direccion)
        VALUES (:tid, :nombre, :apellido, :dui, :direccion)
        """
    )
    try:
        with engine.begin() as conn:
            res = conn.execute(q, {
                "tid": id_tipo_usuario,
                "nombre": nombre,
                "apellido": apellido,
                "dui": dui,
                "direccion": direccion
            })
            # intentar devolver lastrowid cuando esté disponible
            try:
                last = getattr(res, "lastrowid", None)
                return last or True
            except Exception:
                return True
    except SQLAlchemyError as e:
        # opcional: loggear e información de error
        # print("create_member error:", e)
        return None


# -------------------------
# Actualizar miembro
# -------------------------
def update_member(member_id: int,
                  id_tipo_usuario: Optional[int] = None,
                  nombre: Optional[str] = None,
                  apellido: Optional[str] = None,
                  dui: Optional[str] = None,
                  direccion: Optional[str] = None) -> bool:
    """
    Actualiza campos no nulos provistos. Devuelve True si filas afectadas > 0.
    """
    engine = get_engine()

    # construir SET dinámico
    sets = []
    params = {"mid": member_id}
    if id_tipo_usuario is not None:
        sets.append("id_tipo_usuario = :id_tipo_usuario")
        params["id_tipo_usuario"] = id_tipo_usuario
    if nombre is not None:
        sets.append("nombre = :nombre")
        params["nombre"] = nombre
    if apellido is not None:
        sets.append("apellido = :apellido")
        params["apellido"] = apellido
    if dui is not None:
        sets.append("dui = :dui")
        params["dui"] = dui
    if direccion is not None:
        sets.append("direccion = :direccion")
        params["direccion"] = direccion

    if not sets:
        # nada que actualizar
        return False

    set_sql = ", ".join(sets)
    q = text(f"UPDATE miembro SET {set_sql} WHERE id_miembro = :mid")

    try:
        with engine.begin() as conn:
            res = conn.execute(q, params)
            try:
                return (res.rowcount or 0) > 0
            except Exception:
                # drivers distintos pueden comportarse distinto; asumir True si no hay excepción
                return True
    except SQLAlchemyError:
        return False


# -------------------------
# Eliminar miembro
# -------------------------
def delete_member(member_id: int) -> bool:
    engine = get_engine()
    q = text("DELETE FROM miembro WHERE id_miembro = :mid")
    try:
        with engine.begin() as conn:
            res = conn.execute(q, {"mid": member_id})
            try:
                return (res.rowcount or 0) > 0
            except Exception:
                return True
    except SQLAlchemyError:
        return False

