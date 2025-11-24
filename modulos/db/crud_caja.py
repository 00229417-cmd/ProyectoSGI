# modulos/db/crud_caja.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List

def list_movimientos(limit:int = 200) -> List[dict]:
    engine = get_engine()
    q = text("""
        SELECT id_caja, id_ciclo, ingresos, egresos, saldo_final, fecha
        FROM caja
        ORDER BY id_caja DESC
        LIMIT :lim
    """)
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def create_movimiento(id_ciclo:int, tipo:str, monto:float, detalle:str = None):
    engine = get_engine()
    if tipo not in ("ingreso","egreso"):
        raise ValueError("tipo debe ser 'ingreso' o 'egreso'")
    ingresos = monto if tipo=="ingreso" else 0
    egresos = monto if tipo=="egreso" else 0
    q = text("""
        INSERT INTO caja (id_ciclo, ingresos, egresos, saldo_inicial, saldo_final, fecha)
        VALUES (:ciclo, :ing, :eg, 0, :saldo_final, NOW())
    """)
    saldo_final = ingresos - egresos
    with engine.begin() as conn:
        res = conn.execute(q, {"ciclo": id_ciclo, "ing": ingresos, "eg": egresos, "saldo_final": saldo_final})
        try:
            return res.lastrowid or True
        except Exception:
            return True


