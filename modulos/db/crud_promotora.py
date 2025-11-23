# modulos/db/crud_promotora.py
from sqlalchemy import text
from modulos.config.conexion import get_engine

def listar_promotoras(limit=200):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id_promotora, nombre, contacto FROM promotora ORDER BY id_promotora DESC LIMIT :lim")
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def crear_promotora(nombre, contacto=None):
    engine = get_engine()
    with engine.begin() as conn:
        q = text("INSERT INTO promotora (nombre, contacto) VALUES (:n, :c)")
        res = conn.execute(q, {"n": nombre, "c": contacto})
        try:
            return res.lastrowid or True
        except Exception:
            return True
