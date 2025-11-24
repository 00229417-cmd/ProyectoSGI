# modulos/db/crud_config.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List

def list_tipo_usuario(limit:int=200) -> List[dict]:
    engine = get_engine()
    q = text("SELECT id_tipo_usuario, nombre FROM tipo_usuario ORDER BY id_tipo_usuario LIMIT :lim")
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]
