# modulos/db/crud_prestamo.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List, Optional

def list_prestamos(limit: int = 200) -> List[dict]:
    engine = get_engine()
    q = text("""
        SELECT id_prestamo, id_promotora, id_ciclo, id_miembro, monto, intereses, saldo_restante, estado, fecha_solicitud
        FROM prestamo
        ORDER BY id_prestamo DESC
        LIMIT :lim
    """)
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def get_prestamo(id_prestamo: int) -> Optional[dict]:
    engine = get_engine()
    q = text("SELECT * FROM prestamo WHERE id_prestamo = :id LIMIT 1")
    with engine.connect() as conn:
        r = conn.execute(q, {"id": id_prestamo}).mappings().first()
        return dict(r) if r else None

def create_prestamo(id_promotora:int, id_ciclo:int, id_miembro:int, monto:float, intereses:float, plazo_meses:int):
    engine = get_engine()
    q = text("""
        INSERT INTO prestamo (id_promotora, id_ciclo, id_miembro, monto, intereses, saldo_restante, estado, plazo_meses)
        VALUES (:prom, :ciclo, :mem, :monto, :int, :saldo, 'vigente', :plazo)
    """)
    with engine.begin() as conn:
        res = conn.execute(q, {"prom": id_promotora, "ciclo": id_ciclo, "mem": id_miembro, "monto": monto, "int": intereses, "saldo": monto, "plazo": plazo_meses})
        try:
            return res.lastrowid or True
        except Exception:
            return True

def update_prestamo(id_prestamo:int, updates: dict):
    engine = get_engine()
    # ejemplo simple de update (mejor construir dinámico si hay muchos campos)
    q = text("""
        UPDATE prestamo SET monto=:monto, intereses=:intereses WHERE id_prestamo=:id
    """)
    with engine.begin() as conn:
        conn.execute(q, {"monto": updates.get("monto"), "intereses": updates.get("intereses"), "id": id_prestamo})
        return True

