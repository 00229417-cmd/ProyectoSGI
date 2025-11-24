# modulos/db/crud_pago.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List

def list_pagos(limit: int = 200) -> List[dict]:
    engine = get_engine()
    q = text("""
        SELECT id_pago, id_prestamo, id_miembro, monto_pagado, fecha_pago, metodo
        FROM pago
        ORDER BY fecha_pago DESC
        LIMIT :lim
    """)
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def create_pago(id_prestamo:int, id_miembro:int, monto:float, metodo:str="efectivo"):
    engine = get_engine()
    q = text("""
        INSERT INTO pago (id_prestamo, id_miembro, monto_pagado, fecha_pago, metodo)
        VALUES (:prest, :mem, :mto, NOW(), :metodo)
    """)
    with engine.begin() as conn:
        res = conn.execute(q, {"prest": id_prestamo, "mem": id_miembro, "mto": monto, "metodo": metodo})
        try:
            return res.lastrowid or True
        except Exception:
            return True

