# modulos/db/crud_cuota.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List, Optional

def list_cuotas(limit:int=500) -> List[dict]:
    engine = get_engine()
    q = text("""
        SELECT id_cuota, id_prestamo, numero_cuota, fecha_vencimiento, monto, saldo, estado
        FROM cuota
        ORDER BY id_cuota DESC LIMIT :lim
    """)
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def get_cuota(id_cuota:int) -> Optional[dict]:
    engine = get_engine()
    q = text("SELECT * FROM cuota WHERE id_cuota = :id LIMIT 1")
    with engine.connect() as conn:
        r = conn.execute(q, {"id": id_cuota}).mappings().first()
        return dict(r) if r else None

def update_cuota_pay(id_cuota:int, pago:float):
    engine = get_engine()
    q = text("UPDATE cuota SET saldo = saldo - :p WHERE id_cuota = :id")
    with engine.begin() as conn:
        conn.execute(q, {"p": pago, "id": id_cuota})
        return True
