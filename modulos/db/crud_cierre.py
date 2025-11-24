# modulos/db/crud_cierre.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List

def list_cierres(limit:int=100) -> List[dict]:
    engine = get_engine()
    q = text("SELECT id_cierre, id_ciclo, fecha, resumen, estado FROM cierre ORDER BY id_cierre DESC LIMIT :lim")
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def create_cierre(id_ciclo:int, resumen:str):
    engine = get_engine()
    q = text("INSERT INTO cierre (id_ciclo, fecha, resumen, estado) VALUES (:c, NOW(), :r, 'cerrado')")
    with engine.begin() as conn:
        conn.execute(q, {"c": id_ciclo, "r": resumen})
        return True
