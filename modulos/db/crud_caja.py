# modulos/db/crud_caja.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from datetime import datetime

def registrar_movimiento(tipo, monto, detalle, fecha=None):
    engine = get_engine()
    if fecha is None:
        fecha = datetime.utcnow().strftime("%Y-%m-%d")
    with engine.begin() as conn:
        q = text("INSERT INTO caja_movimiento (tipo, monto, detalle, fecha) VALUES (:t, :m, :d, :f)")
        res = conn.execute(q, {"t": tipo, "m": monto, "d": detalle, "f": fecha})
        try:
            return res.lastrowid or True
        except Exception:
            return True

def listar_movimientos(limit=100):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id, tipo, monto, detalle, fecha FROM caja_movimiento ORDER BY fecha DESC LIMIT :lim")
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def obtener_saldo_actual():
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT SUM(CASE WHEN tipo = 'ingreso' THEN monto ELSE -monto END) as saldo FROM caja_movimiento")
        r = conn.execute(q).mappings().first()
        return float(r["saldo"]) if r and r["saldo"] is not None else 0.0

