# modulos/db/crud_ciclo.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List

def list_ciclos(limit:int=200) -> List[dict]:
    engine = get_engine()
    q = text("SELECT id_ciclo, nombre, fecha_inicio, fecha_fin, estado FROM ciclo ORDER BY id_ciclo DESC LIMIT :lim")
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def create_ciclo(nombre:str, fecha_inicio:str, fecha_fin:str):
    engine = get_engine()
    q = text("INSERT INTO ciclo (nombre, fecha_inicio, fecha_fin, estado) VALUES (:n, :fi, :ff, 'activo')")
    with engine.begin() as conn:
        conn.execute(q, {"n": nombre, "fi": fecha_inicio, "ff": fecha_fin})
        return True
