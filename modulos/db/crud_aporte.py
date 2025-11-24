# modulos/db/crud_aporte.py
from typing import List, Dict, Any, Optional
from sqlalchemy import text
from modulos.config.conexion import get_engine
import datetime

ENGINE = get_engine()

def list_aportes(limit: int = 500) -> List[Dict[str, Any]]:
    """
    Devuelve una lista de aportes como lista de diccionarios.
    """
    sql = text("""
        SELECT id_aporte, id_miembro, id_reunion, monto, fecha, tipo
        FROM aporte
        ORDER BY id_aporte DESC
        LIMIT :lim
    """)
    with ENGINE.connect() as conn:
        res = conn.execute(sql, {"lim": limit})
        rows = [dict(r) for r in res.mappings().all()]
    return rows

def create_aporte(
    id_miembro: int,
    id_reunion: Optional[int],
    monto: float,
    fecha: datetime.date,
    tipo: str
) -> int:
    """
    Inserta un aporte y devuelve el id_insertado.
    Firma diseñada para recibir los 5 campos individualmente.
    """
    sql = text("""
        INSERT INTO aporte (id_miembro, id_reunion, monto, fecha, tipo)
        VALUES (:id_miembro, :id_reunion, :monto, :fecha, :tipo)
    """)
    # normalizar fecha a string si es date
    fecha_val = fecha.isoformat() if hasattr(fecha, "isoformat") else fecha

    with ENGINE.begin() as conn:  # begin() para commit automático o rollback
        r = conn.execute(sql, {
            "id_miembro": id_miembro,
            "id_reunion": id_reunion,
            "monto": monto,
            "fecha": fecha_val,
            "tipo": tipo
        })
        # obtener lastrowid (compatible con mysqlconnector)
        try:
            inserted_id = r.lastrowid
        except Exception:
            # fallback: ejecutar SELECT LAST_INSERT_ID()
            last = conn.execute(text("SELECT LAST_INSERT_ID() AS id")).mappings().first()
            inserted_id = int(last["id"]) if last else 0

    return int(inserted_id)

