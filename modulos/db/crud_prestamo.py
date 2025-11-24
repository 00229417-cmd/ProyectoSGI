# modulos/db/crud_prestamo.py
from sqlalchemy import text
from modulos.config.conexion import get_engine

def listar_prestamos(limit: int = 500):
    """
    Retorna una lista de diccionarios: [{col: val, ...}, ...]
    Siempre devuelve lista (puede estar vacía).
    """
    engine = get_engine()
    query = text("""
        SELECT
            id_prestamo,
            id_promotora,
            id_ciclo,
            id_miembro,
            monto,
            intereses,
            saldo_restante,
            estado,
            plazo_meses,
            total_cuotas,
            fecha_solicitud
        FROM prestamo
        ORDER BY id_prestamo DESC
        LIMIT :lim
    """)
    with engine.connect() as conn:
        # .mappings().all() devuelve lista de RowMapping -> convertibles a dict
        result = conn.execute(query, {"lim": limit})
        rows = result.mappings().all()
        # Aseguramos convertir cada RowMapping a dict simple
        return [dict(r) for r in rows]

def create_prestamo(
    id_ciclo: int,
    id_miembro: int,
    monto: float,
    intereses: float,
    plazo_meses: int,
    id_promotora: int | None = None,
    fecha_solicitud: str | None = None
):
    """
    Inserta un préstamo y devuelve el id insertado (int) o None en caso de fallo.
    """
    engine = get_engine()
    insert_sql = text("""
        INSERT INTO prestamo (
            id_promotora,
            id_ciclo,
            id_miembro,
            monto,
            intereses,
            saldo_restante,
            estado,
            plazo_meses,
            total_cuotas,
            fecha_solicitud
        ) VALUES (
            :id_promotora, :id_ciclo, :id_miembro, :monto, :intereses, :saldo_restante,
            :estado, :plazo_meses, :total_cuotas, :fecha_solicitud
        )
    """)
    # saldo_restante = monto al inicio; total_cuotas = plazo_meses (o calcular según tu lógica)
    params = {
        "id_promotora": id_promotora,
        "id_ciclo": id_ciclo,
        "id_miembro": id_miembro,
        "monto": monto,
        "intereses": intereses,
        "saldo_restante": monto,
        "estado": "pendiente",
        "plazo_meses": plazo_meses,
        "total_cuotas": plazo_meses,
        "fecha_solicitud": fecha_solicitud
    }
    with engine.begin() as conn:
        res = conn.execute(insert_sql, params)
        # Obtener LAST_INSERT_ID de MySQL/MariaDB
        last_id = conn.execute(text("SELECT LAST_INSERT_ID() AS id")).scalar()
        try:
            return int(last_id)
        except Exception:
            return None
