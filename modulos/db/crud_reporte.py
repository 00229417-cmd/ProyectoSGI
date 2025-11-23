# modulos/db/crud_reporte.py
from sqlalchemy import text
from modulos.config.conexion import get_engine

def reporte_resumen_operativo():
    engine = get_engine()
    with engine.connect() as conn:
        # ejemplo: totales rápidos
        q1 = text("SELECT COUNT(*) as total_miembros FROM miembro")
        q2 = text("SELECT COUNT(*) as prestamos_vigentes FROM prestamo WHERE estado <> 'cancelado'")
        r1 = conn.execute(q1).mappings().first()
        r2 = conn.execute(q2).mappings().first()
        return {
            "total_miembros": int(r1["total_miembros"]) if r1 else 0,
            "prestamos_vigentes": int(r2["prestamos_vigentes"]) if r2 else 0
        }
