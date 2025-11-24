# modulos/db/crud_reporte.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List, Dict, Any, Optional

def list_reportes(limit: int = 200) -> List[Dict[str, Any]]:
    """
    Lista reportes usando las columnas reales del ER: 
    id_reporte, id_ciclo, id_administrador, tipo, fecha_generacion, descripcion, estado
    """
    engine = get_engine()
    q = text("""
        SELECT id_reporte, id_ciclo, id_administrador, tipo, fecha_generacion, descripcion, estado
        FROM reporte
        ORDER BY id_reporte DESC
        LIMIT :lim
    """)
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def get_reporte(id_reporte: int) -> Optional[Dict[str, Any]]:
    engine = get_engine()
    q = text("""
        SELECT id_reporte, id_ciclo, id_administrador, tipo, fecha_generacion, descripcion, estado
        FROM reporte
        WHERE id_reporte = :id
        LIMIT 1
    """)
    with engine.connect() as conn:
        r = conn.execute(q, {"id": id_reporte}).mappings().first()
        return dict(r) if r else None

def create_reporte(id_ciclo: int = None,
                   id_administrador: int = None,
                   tipo: str = None,
                   descripcion: str = None,
                   estado: str = "pendiente") -> bool:
    """
    Inserta un reporte. La fecha se toma con NOW() en la columna fecha_generacion.
    Sólo inserta las columnas que el ER define.
    """
    engine = get_engine()
    q = text("""
        INSERT INTO reporte (id_ciclo, id_administrador, tipo, fecha_generacion, descripcion, estado)
        VALUES (:id_ciclo, :id_adm, :tipo, NOW(), :desc, :estado)
    """)
    params = {
        "id_ciclo": id_ciclo,
        "id_adm": id_administrador,
        "tipo": tipo,
        "desc": descripcion,
        "estado": estado
    }
    with engine.begin() as conn:
        conn.execute(q, params)
        return True
