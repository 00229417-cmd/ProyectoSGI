# modulos/db/crud_asistencia.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import List, Optional

def list_asistencias(limit: int = 500) -> List[dict]:
    """Lista asistencias con las columnas existentes en la BD."""
    engine = get_engine()
    q = text("""
        SELECT
            id_asistencia,
            id_miembro,
            id_reunion,
            id_multa,
            motivo,
            presente_ausente,
            fecha
        FROM asistencia
        ORDER BY id_asistencia DESC
        LIMIT :lim
    """)
    with engine.connect() as conn:
        rs = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rs]

def record_asistencia(
    id_reunion: int,
    id_miembro: int,
    presente_ausente: bool = True,
    id_multa: Optional[int] = None,
    motivo: Optional[str] = None
) -> bool:
    """
    Inserta una asistencia. id_multa y motivo son opcionales según tu modelo.
    presente_ausente se guarda como 1/0.
    """
    engine = get_engine()
    q = text("""
        INSERT INTO asistencia (
            id_reunion,
            id_miembro,
            id_multa,
            motivo,
            presente_ausente,
            fecha
        ) VALUES (
            :id_reunion, :id_miembro, :id_multa, :motivo, :presente, NOW()
        )
    """)
    params = {
        "id_reunion": id_reunion,
        "id_miembro": id_miembro,
        "id_multa": id_multa,
        "motivo": motivo,
        "presente": 1 if presente_ausente else 0
    }
    with engine.begin() as conn:
        conn.execute(q, params)
    return True
