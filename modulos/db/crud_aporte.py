# modulos/db/crud_aporte.py
from typing import List, Dict, Any, Optional
from sqlalchemy import text
from modulos.config.conexion import get_engine

# ----------------------------
# LISTAR / OBTENER
# ----------------------------
def list_aportes(limit: int = 500) -> List[Dict[str, Any]]:
    """
    Retorna lista de aportes como lista de dicts.
    Columnas esperadas en la tabla 'aporte':
      id_aporte, id_miembro, id_reunion, monto, fecha, tipo
    """
    sql = text("""
        SELECT
            id_aporte,
            id_miembro,
            id_reunion,
            monto,
            fecha,
            tipo
        FROM aporte
        ORDER BY id_aporte DESC
        LIMIT :lim
    """)
    engine = get_engine()
    try:
        with engine.connect() as conn:
            res = conn.execute(sql, {"lim": limit})
            return res.mappings().all()
    except Exception:
        return []

def obtener_aporte_por_id(id_aporte: int) -> Optional[Dict[str, Any]]:
    sql = text("""
        SELECT
            id_aporte,
            id_miembro,
            id_reunion,
            monto,
            fecha,
            tipo
        FROM aporte
        WHERE id_aporte = :id_aporte
        LIMIT 1
    """)
    engine = get_engine()
    try:
        with engine.connect() as conn:
            res = conn.execute(sql, {"id_aporte": id_aporte})
            return res.mappings().first()
    except Exception:
        return None

# ----------------------------
# CREAR (español) + ALIAS en inglés para compatibilidad
# ----------------------------
def crear_aporte(data: Dict[str, Any]) -> int:
    """
    data debe contener: id_miembro, id_reunion, monto, fecha, tipo
    Retorna id_insertado (int) o 0 si falla.
    """
    sql = text("""
        INSERT INTO aporte (
            id_miembro,
            id_reunion,
            monto,
            fecha,
            tipo
        ) VALUES (
            :id_miembro,
            :id_reunion,
            :monto,
            :fecha,
            :tipo
        )
    """)
    engine = get_engine()
    try:
        with engine.begin() as conn:
            res = conn.execute(sql, data)
            # SQLAlchemy DBAPI res.lastrowid puede no estar presente en todos los backends;
            # intentar extraerlo de formas seguras:
            try:
                last = int(res.lastrowid) if hasattr(res, "lastrowid") and res.lastrowid else 0
            except Exception:
                last = 0
            return last
    except Exception:
        return 0

# alias en inglés — muchas páginas esperan este nombre
def create_aporte(data: Dict[str, Any]) -> int:
    return crear_aporte(data)

# ----------------------------
# ACTUALIZAR
# ----------------------------
def actualizar_aporte(id_aporte: int, data: Dict[str, Any]) -> bool:
    """
    Actualiza un aporte por id_aporte.
    data puede contener id_miembro, id_reunion, monto, fecha, tipo
    """
    sql = text("""
        UPDATE aporte
        SET
            id_miembro = :id_miembro,
            id_reunion = :id_reunion,
            monto = :monto,
            fecha = :fecha,
            tipo = :tipo
        WHERE id_aporte = :id_aporte
    """)
    params = dict(data)
    params["id_aporte"] = id_aporte
    engine = get_engine()
    try:
        with engine.begin() as conn:
            res = conn.execute(sql, params)
            return res.rowcount > 0
    except Exception:
        return False

# alias en inglés
def update_aporte(id_aporte: int, data: Dict[str, Any]) -> bool:
    return actualizar_aporte(id_aporte, data)

# ----------------------------
# ELIMINAR
# ----------------------------
def eliminar_aporte(id_aporte: int) -> bool:
    sql = text("DELETE FROM aporte WHERE id_aporte = :id_aporte")
    engine = get_engine()
    try:
        with engine.begin() as conn:
            res = conn.execute(sql, {"id_aporte": id_aporte})
            return res.rowcount > 0
    except Exception:
        return False

# alias en inglés
def delete_aporte(id_aporte: int) -> bool:
    return eliminar_aporte(id_aporte)

# ----------------------------
# SELECT AUX (reuniones para selects)
# ----------------------------
def list_reuniones_para_select(limit: int = 200) -> List[Dict[str, Any]]:
    """
    Lista mínima de reuniones para poblar selects: id_reunion, fecha, lugar.
    Devuelve [] si la tabla no existe o falla.
    """
    sql = text("""
        SELECT id_reunion, fecha, lugar
        FROM reunion
        ORDER BY fecha DESC
        LIMIT :lim
    """)
    engine = get_engine()
    try:
        with engine.connect() as conn:
            res = conn.execute(sql, {"lim": limit})
            return res.mappings().all()
    except Exception:
        return []
