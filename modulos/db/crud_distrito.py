# modulos/db/crud_distrito.py
from sqlalchemy import text
from modulos.config.conexion import get_engine

def listar_distritos(limit=200):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id_distrito, nombre FROM distrito ORDER BY nombre LIMIT :lim")
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def crear_distrito(nombre):
    engine = get_engine()
    with engine.begin() as conn:
        q = text("INSERT INTO distrito (nombre) VALUES (:n)")
        res = conn.execute(q, {"n": nombre})
        try:
            return res.lastrowid or True
        except Exception:
            return True
