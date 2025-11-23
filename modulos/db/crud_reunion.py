# modulos/db/crud_reunion.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from datetime import datetime

def crear_reunion(id_ciclo, fecha, lugar, descripcion=None):
    engine = get_engine()
    with engine.begin() as conn:
        q = text("INSERT INTO reunion (id_ciclo, fecha, lugar, descripcion) VALUES (:cid, :f, :l, :d)")
        res = conn.execute(q, {"cid": id_ciclo, "f": fecha, "l": lugar, "d": descripcion})
        try:
            return res.lastrowid or True
        except Exception:
            return True

def listar_reuniones(limit=100):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id_reunion, id_ciclo, fecha, lugar, descripcion FROM reunion ORDER BY fecha DESC LIMIT :lim")
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

# Asistencia y multas (sencillo)
def registrar_asistencia(id_reunion, id_miembro, presente=True, multa=0.0):
    engine = get_engine()
    with engine.begin() as conn:
        q = text("INSERT INTO asistencia (id_reunion, id_miembro, presente, multa) VALUES (:rid, :mid, :pre, :mul)")
        res = conn.execute(q, {"rid": id_reunion, "mid": id_miembro, "pre": int(presente), "mul": multa})
        return True
