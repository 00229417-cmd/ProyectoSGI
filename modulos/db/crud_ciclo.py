# modulos/db/crud_ciclo.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from datetime import date

def listar_ciclos(limit=100):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id_ciclo, nombre, fecha_inicio, fecha_fin FROM ciclo ORDER BY id_ciclo DESC LIMIT :lim")
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def crear_ciclo(nombre, fecha_inicio, fecha_fin):
    engine = get_engine()
    with engine.begin() as conn:
        q = text("INSERT INTO ciclo (nombre, fecha_inicio, fecha_fin) VALUES (:n, :fi, :ff)")
        res = conn.execute(q, {"n": nombre, "fi": fecha_inicio, "ff": fecha_fin})
        try:
            return res.lastrowid or True
        except Exception:
            return True
