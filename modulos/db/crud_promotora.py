# modulos/db/crud_promotora.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List

def list_promotoras(limit:int=200) -> List[dict]:
    engine = get_engine()
    q = text("SELECT id_promotora, nombre, contacto FROM promotora ORDER BY id_promotora DESC LIMIT :lim")
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def create_promotora(nombre:str, contacto:str=None):
    engine = get_engine()
    q = text("INSERT INTO promotora (nombre, contacto) VALUES (:n, :c)")
    with engine.begin() as conn:
        conn.execute(q, {"n": nombre, "c": contacto})
        return True
