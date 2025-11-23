# modulos/db/crud_directiva.py
from sqlalchemy import text
from modulos.config.conexion import get_engine

def listar_directiva(id_grupo):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id_directiva, id_grupo, cargo, id_miembro FROM directiva WHERE id_grupo = :gid")
        rows = conn.execute(q, {"gid": id_grupo}).mappings().all()
        return [dict(r) for r in rows]

def asignar_cargo(id_grupo, id_miembro, cargo):
    engine = get_engine()
    with engine.begin() as conn:
        q = text("INSERT INTO directiva (id_grupo, id_miembro, cargo) VALUES (:g, :m, :c)")
        res = conn.execute(q, {"g": id_grupo, "m": id_miembro, "c": cargo})
        try:
            return res.lastrowid or True
        except Exception:
            return True
