# modulos/db/crud_ahorro.py
from sqlalchemy import text
from modulos.config.conexion import get_engine

def obtener_saldo_miembro(id_miembro):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT saldo FROM ahorro WHERE id_miembro = :mid LIMIT 1")
        r = conn.execute(q, {"mid": id_miembro}).mappings().first()
        return r["saldo"] if r else 0.0

def actualizar_saldo(id_miembro, nuevo_saldo):
    engine = get_engine()
    with engine.begin() as conn:
        q = text("UPDATE ahorro SET saldo = :s WHERE id_miembro = :mid")
        res = conn.execute(q, {"s": nuevo_saldo, "mid": id_miembro})
        return res.rowcount > 0
