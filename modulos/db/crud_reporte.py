# modulos/db/crud_reporte.py
from modulos.config.conexion import get_engine
from sqlalchemy import text
from typing import Tuple, List

def list_reportes(limit: int = 200) -> List[dict]:
    q = text("SELECT id_reporte, id_ciclo, id_administrador, tipo, fecha_generacion, descripcion, estado FROM reporte ORDER BY id_reporte DESC LIMIT :lim")
    engine = get_engine()
    with engine.connect() as conn:
        res = conn.execute(q, {"lim": limit})
        rows = [dict(row._mapping) for row in res.fetchall()]
    return rows

def create_reporte(id_ciclo: int | None, id_administrador: int | None, tipo: str = "mora", descripcion: str | None = None) -> Tuple[bool, str]:
    """
    Crea un reporte. id_ciclo debe ser INT o NULL; id_administrador INT o NULL.
    Devuelve (True, "") si OK o (False, mensaje_error).
    """
    q = text("""
        INSERT INTO reporte (id_ciclo, id_administrador, tipo, fecha_generacion, descripcion, estado)
        VALUES (:id_ciclo, :id_adm, :tipo, NOW(), :desc, :estado)
    """)
    params = {
        "id_ciclo": id_ciclo,
        "id_adm": id_administrador,
        "tipo": tipo,
        "desc": descripcion,
        "estado": "pendiente"
    }
    engine = get_engine()
    try:
        with engine.connect() as conn:
            conn.execute(q, params)
        return True, ""
    except Exception as e:
        return False, str(e)
