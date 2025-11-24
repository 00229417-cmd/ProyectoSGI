# modulos/db/crud_reporte.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List

def list_reportes(limit:int=200) -> List[dict]:
    engine = get_engine()
    q = text("SELECT id_reporte, tipo, fecha, usuario, descripcion FROM reporte ORDER BY id_reporte DESC LIMIT :lim")
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def create_reporte(tipo:str, usuario:str, descripcion:str=None):
    engine = get_engine()
    q = text("INSERT INTO reporte (tipo, fecha, usuario, descripcion) VALUES (:t, NOW(), :u, :d)")
    with engine.begin() as conn:
        conn.execute(q, {"t": tipo, "u": usuario, "d": descripcion})
        return True
