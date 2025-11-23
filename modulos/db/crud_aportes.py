# modulos/db/crud_aporte.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from datetime import datetime

def registrar_aporte(id_miembro, monto, fecha=None, tipo="aporte"):
    engine = get_engine()
    if fecha is None:
        fecha = datetime.utcnow().strftime("%Y-%m-%d")
    with engine.begin() as conn:
        q = text("INSERT INTO aporte (id_miembro, monto, fecha, tipo) VALUES (:mid, :m, :f, :t)")
        res = conn.execute(q, {"mid": id_miembro, "m": monto, "f": fecha, "t": tipo})
        try:
            return res.lastrowid or True
        except Exception:
            return True

def listar_aportes(limit=100):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id_aporte, id_miembro, monto, fecha, tipo FROM aporte ORDER BY fecha DESC LIMIT :lim")
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

