# modulos/db/crud_logs.py
from sqlalchemy import text
from modulos.config.conexion import get_engine

# =====================================================
# LISTAR LOGS
# =====================================================
def list_logs(limit: int = 200):
    """
    Devuelve lista de logs desde la tabla activity_logs.
    Requiere columnas mínimas:
        id_log, user_id, action, timestamp, details
    """
    engine = get_engine()
    q = text("""
        SELECT
            id_log,
            user_id,
            action,
            timestamp,
            details
        FROM activity_logs
        ORDER BY id_log DESC
        LIMIT :lim
    """)

    try:
        with engine.connect() as conn:
            rows = conn.execute(q, {"lim": limit}).mappings().all()
            return [dict(r) for r in rows]
    except Exception as e:
        print("Error list_logs():", e)
        return []


# =====================================================
# CREAR LOG (opcional pero muy útil)
# =====================================================
def add_log(user_id: int | None, action: str, details: str = None) -> bool:
    """
    Inserta un registro en activity_logs.
    Puedes llamarla manualmente desde cualquier parte de tu app.
    """
    engine = get_engine()
    q = text("""
        INSERT INTO activity_logs (user_id, action, details)
        VALUES (:uid, :ac, :dt)
    """)

    try:
        with engine.begin() as conn:
            conn.execute(q, {
                "uid": user_id,
                "ac": action,
                "dt": details,
            })
        return True
    except Exception as e:
        print("Error add_log():", e)
        return False
