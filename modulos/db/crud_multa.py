# modulos/db/crud_multa.py
from sqlalchemy import text
from modulos.config.conexion import get_engine

def crear_multa(id_miembro, id_reunion, monto, descripcion=None):
    engine = get_engine()
    with engine.begin() as conn:
        q = text("INSERT INTO multa (id_miembro, id_reunion, monto, descripcion) VALUES (:mid, :rid, :m, :d)")
        res = conn.execute(q, {"mid": id_miembro, "rid": id_reunion, "m": monto, "d": descripcion})
        try:
            return res.lastrowid or True
        except Exception:
            return True

def listar_multas(limit=200):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id_multa, id_miembro, id_reunion, monto, descripcion FROM multa ORDER BY id_multa DESC LIMIT :lim")
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

