# modulos/db/crud_caja.py
from sqlalchemy import text
from modulos.config.conexion import get_engine

def list_caja(limit: int = 200):
    """
    Devuelve lista de dicts con los movimientos/entradas de la tabla 'caja'.
    Asegúrate que las columnas en la BD coincidan con las usadas aquí.
    """
    engine = get_engine()
    q = text("""
        SELECT
            id_caja,
            id_ciclo,
            id_ahorro,
            id_prestamo,
            id_pago,
            saldo_inicial,
            ingresos,
            egresos,
            saldo_final
        FROM caja
        ORDER BY id_caja DESC
        LIMIT :lim
    """)
    with engine.connect() as conn:
        r = conn.execute(q, {"lim": limit})
        rows = r.mappings().all()
        return [dict(row) for row in rows]

def create_caja(
    id_ciclo: int | None,
    id_ahorro: int | None,
    id_prestamo: int | None,
    id_pago: int | None,
    saldo_inicial: float,
    ingresos: float,
    egresos: float,
):
    """
    Inserta un registro en caja y devuelve el id insertado (int) o None.
    saldo_final se calcula: saldo_inicial + ingresos - egresos
    """
    engine = get_engine()
    saldo_final = float(saldo_inicial) + float(ingresos) - float(egresos)
    insert = text("""
        INSERT INTO caja (
            id_ciclo, id_ahorro, id_prestamo, id_pago,
            saldo_inicial, ingresos, egresos, saldo_final
        ) VALUES (
            :id_ciclo, :id_ahorro, :id_prestamo, :id_pago,
            :saldo_inicial, :ingresos, :egresos, :saldo_final
        )
    """)
    params = {
        "id_ciclo": id_ciclo,
        "id_ahorro": id_ahorro,
        "id_prestamo": id_prestamo,
        "id_pago": id_pago,
        "saldo_inicial": saldo_inicial,
        "ingresos": ingresos,
        "egresos": egresos,
        "saldo_final": saldo_final,
    }
    with engine.begin() as conn:
        conn.execute(insert, params)
        last_id = conn.execute(text("SELECT LAST_INSERT_ID() AS id")).scalar()
        try:
            return int(last_id)
        except Exception:
            return None

def get_caja_by_id(id_caja: int):
    engine = get_engine()
    q = text("SELECT * FROM caja WHERE id_caja = :id LIMIT 1")
    with engine.connect() as conn:
        r = conn.execute(q, {"id": id_caja}).mappings().first()
        return dict(r) if r else None


