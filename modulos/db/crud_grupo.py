# modulos/db/crud_grupo.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from datetime import datetime

def listar_grupos(limit=200):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id_grupo, nombre, descripcion, fecha_creacion FROM grupo ORDER BY id_grupo DESC LIMIT :lim")
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def crear_grupo(nombre, descripcion=None):
    engine = get_engine()
    with engine.begin() as conn:
        q = text("INSERT INTO grupo (nombre, descripcion, fecha_creacion) VALUES (:n, :d, :f)")
        res = conn.execute(q, {"n": nombre, "d": descripcion, "f": datetime.utcnow().strftime("%Y-%m-%d")})
        try:
            return res.lastrowid or True
        except Exception:
            return True

def obtener_grupo(id_grupo):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT * FROM grupo WHERE id_grupo = :id LIMIT 1")
        r = conn.execute(q, {"id": id_grupo}).mappings().first()
        return dict(r) if r else None
