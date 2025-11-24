# modulos/db/crud_asistencia.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List

def list_asistencias(limit:int=500) -> List[dict]:
    engine = get_engine()
    q = text("SELECT id_asistencia, id_reunion, id_miembro, presente, observaciones FROM asistencia ORDER BY id_asistencia DESC LIMIT :lim")
    with engine.connect() as conn:
        rs = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rs]

def record_asistencia(id_reunion:int, id_miembro:int, presente:bool=True, observaciones:str=None):
    engine = get_engine()
    q = text("INSERT INTO asistencia (id_reunion, id_miembro, presente, observaciones, fecha) VALUES (:r, :m, :p, :o, NOW())")
    with engine.begin() as conn:
        conn.execute(q, {"r": id_reunion, "m": id_miembro, "p": int(bool(presente)), "o": observaciones})
        return True
