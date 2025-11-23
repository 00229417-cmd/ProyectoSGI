# modulos/db/crud_cierre.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from datetime import datetime

def registrar_cierre(id_ciclo, resumen, fecha=None):
    engine = get_engine()
    if fecha is None:
        fecha = datetime.utcnow().strftime("%Y-%m-%d")
    with engine.begin() as conn:
        q = text("INSERT INTO cierre (id_ciclo, resumen, fecha) VALUES (:cid, :res, :f)")
        res = conn.execute(q, {"cid": id_ciclo, "res": resumen, "f": fecha})
        try:
            return res.lastrowid or True
        except Exception:
            return True
