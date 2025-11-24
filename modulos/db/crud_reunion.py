# modulos/db/crud_reunion.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List

def list_reuniones(limit:int=200) -> List[dict]:
    engine = get_engine()
    q = text("SELECT id_reunion, id_ciclo, fecha, lugar, descripcion FROM reunion ORDER BY id_reunion DESC LIMIT :lim")
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def create_reunion(id_ciclo:int, fecha:str, lugar:str, descripcion:str=None):
    engine = get_engine()
    q = text("INSERT INTO reunion (id_ciclo, fecha, lugar, descripcion) VALUES (:c, :f, :l, :d)")
    with engine.begin() as conn:
        conn.execute(q, {"c": id_ciclo, "f": fecha, "l": lugar, "d": descripcion})
        return True
