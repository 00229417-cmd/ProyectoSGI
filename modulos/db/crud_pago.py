# modulos/db/crud_pago.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from datetime import datetime

def registrar_pago(id_cuota, id_miembro, monto, fecha=None, metodo="efectivo"):
    engine = get_engine()
    if fecha is None:
        fecha = datetime.utcnow().strftime("%Y-%m-%d")
    with engine.begin() as conn:
        q = text("INSERT INTO pago (id_cuota, id_miembro, monto, fecha, metodo) VALUES (:cid, :mid, :m, :f, :met)")
        res = conn.execute(q, {"cid": id_cuota, "mid": id_miembro, "m": monto, "f": fecha, "met": metodo})
        # actualizar cuota a pagada si corresponde
        try:
            # marcar cuota como pagada (si monto >= cuota.monto) — simplificación
            conn.execute(text("UPDATE cuota SET estado = 'pagada' WHERE id = :cid"), {"cid": id_cuota})
        except Exception:
            pass
        try:
            return res.lastrowid or True
        except Exception:
            return True

