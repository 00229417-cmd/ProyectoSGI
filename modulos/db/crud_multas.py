# modulos/db/crud_multas.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List, Optional

def list_multas(limit: int = 200) -> List[dict]:
    engine = get_engine()
    q = text("""
        SELECT
            id_multa,
            id_miembro,
            tipo,
            monto,
            descripcion,
            fecha,
            estado
        FROM multa
        ORDER BY id_multa DESC
        LIMIT :lim
    """)
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def create_multa(id_miembro: int,
                 monto: float,
                 tipo: Optional[str] = None,
                 descripcion: Optional[str] = None,
                 id_reunion: Optional[int] = None) -> bool:
    """
    Crea una multa. tipo/descripcion/id_reunion son opcionales segun tu modelo.
    estado por defecto 'pendiente'.
    """
    engine = get_engine()
    q = text("""
        INSERT INTO multa (
            id_miembro,
            id_reunion,
            tipo,
            monto,
            descripcion,
            fecha,
            estado
        ) VALUES (
            :id_miembro, :id_reunion, :tipo, :monto, :descripcion, NOW(), 'pendiente'
        )
    """)
    params = {
        "id_miembro": id_miembro,
        "id_reunion": id_reunion,
        "tipo": tipo,
        "monto": monto,
        "descripcion": descripcion
    }
    with engine.begin() as conn:
        conn.execute(q, params)
    return True
