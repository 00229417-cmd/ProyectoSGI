# modulos/db/crud_grupo.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List

def list_grupos(limit:int=200) -> List[dict]:
    engine = get_engine()
    q = text("SELECT id_grupo, nombre, descripcion FROM grupo ORDER BY id_grupo DESC LIMIT :lim")
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def create_grupo(nombre:str, descripcion:str=None):
    engine = get_engine()
    q = text("INSERT INTO grupo (nombre, descripcion) VALUES (:n, :d)")
    with engine.begin() as conn:
        conn.execute(q, {"n": nombre, "d": descripcion})
        return True
