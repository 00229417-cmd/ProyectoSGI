# modulos/db/crud_ahorro.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List

def list_aportes(limit: int = 500) -> List[dict]:
    engine = get_engine()
    q = text("""
        SELECT id_ahorro AS id, id_miembro, id_ciclo, monto, fecha, tipo, descripcion
        FROM ahorro
        ORDER BY id_ahorro DESC
        LIMIT :lim
    """)
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def create_aporte(id_miembro:int, id_ciclo:int, monto:float, tipo:str="aporte", descripcion:str=None):
    engine = get_engine()
    q = text("""
        INSERT INTO ahorro (id_miembro, id_ciclo, monto, fecha, tipo, descripcion)
        VALUES (:m, :c, :mo, NOW(), :t, :d)
    """)
    with engine.begin() as conn:
        res = conn.execute(q, {"m": id_miembro, "c": id_ciclo, "mo": monto, "t": tipo, "d": descripcion})
        try:
            return res.lastrowid or True
        except Exception:
            return True
