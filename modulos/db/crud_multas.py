# modulos/db/crud_multas.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List

def list_multas(limit:int=200) -> List[dict]:
    engine = get_engine()
    q = text("SELECT id_multa, id_miembro, id_reunion, monto, motivo, estado FROM multa ORDER BY id_multa DESC LIMIT :lim")
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def create_multa(id_miembro:int, id_reunion:int, monto:float, motivo:str):
    engine = get_engine()
    q = text("INSERT INTO multa (id_miembro, id_reunion, monto, motivo, estado) VALUES (:m, :r, :mo, :mot, 'pendiente')")
    with engine.begin() as conn:
        conn.execute(q, {"m": id_miembro, "r": id_reunion, "mo": monto, "mot": motivo})
        return True
