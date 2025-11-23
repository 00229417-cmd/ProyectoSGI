# modulos/db/crud_acta.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from datetime import datetime

def crear_acta(id_ciclo, titulo, contenido, fecha=None):
    engine = get_engine()
    if fecha is None:
        fecha = datetime.utcnow().strftime("%Y-%m-%d")
    with engine.begin() as conn:
        q = text("INSERT INTO acta (id_ciclo, titulo, contenido, fecha) VALUES (:cid, :t, :c, :f)")
        res = conn.execute(q, {"cid": id_ciclo, "t": titulo, "c": contenido, "f": fecha})
        try:
            return res.lastrowid or True
        except Exception:
            return True
