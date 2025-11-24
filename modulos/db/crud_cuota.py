# modulos/db/crud_cuota.py
from modulos.config.conexion import get_engine
from sqlalchemy import text

def obtener_cuotas(limit=500):
    sql = text("""
        SELECT 
            id_cuota,
            id_prestamo,
            numero_cuota,
            fecha_vencimiento,
            monto_capital,
            monto_interes,
            monto_total,
            estado
        FROM cuota
        ORDER BY id_cuota DESC
        LIMIT :lim
    """)

    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(sql, {"lim": limit})
        rows = result.mappings().all()

    return rows


def crear_cuota(data: dict):
    sql = text("""
        INSERT INTO cuota (
            id_prestamo,
            fecha_vencimiento,
            numero_cuota,
            monto_capital,
            monto_interes,
            monto_total,
            estado
        )
        VALUES (
            :id_prestamo,
            :fecha_vencimiento,
            :numero_cuota,
            :monto_capital,
            :monto_interes,
            :monto_total,
            :estado
        )
    """)

    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(sql, data)
        return True
