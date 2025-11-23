# modulos/db/crud_cuota.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from datetime import datetime

def generar_cuota(id_prestamo, numero, fecha_vencimiento, monto):
    engine = get_engine()
    with engine.begin() as conn:
        q = text("INSERT INTO cuota (id_prestamo, numero, fecha_vencimiento, monto, estado) VALUES (:pid, :num, :fv, :m, 'pendiente')")
        res = conn.execute(q, {"pid": id_prestamo, "num": numero, "fv": fecha_vencimiento, "m": monto})
        try:
            return res.lastrowid or True
        except Exception:
            return True

def listar_cuotas_prestamo(id_prestamo):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT * FROM cuota WHERE id_prestamo = :pid ORDER BY numero ASC")
        rows = conn.execute(q, {"pid": id_prestamo}).mappings().all()
        return [dict(r) for r in rows]
