# modulos/db/crud_prestamo.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from datetime import datetime

def solicitar_prestamo(id_miembro, monto, plazo_meses, tasa_interes, fecha_solicitud=None):
    engine = get_engine()
    if fecha_solicitud is None:
        fecha_solicitud = datetime.utcnow().strftime("%Y-%m-%d")
    with engine.begin() as conn:
        q = text("""INSERT INTO prestamo (id_miembro, monto, plazo_meses, tasa_interes, fecha_solicitud, estado)
                    VALUES (:mid, :m, :p, :t, :f, 'pendiente')""")
        res = conn.execute(q, {"mid": id_miembro, "m": monto, "p": plazo_meses, "t": tasa_interes, "f": fecha_solicitud})
        try:
            return res.lastrowid or True
        except Exception:
            return True

def listar_prestamos(limit=200):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id_prestamo, id_miembro, monto, plazo_meses, tasa_interes, estado FROM prestamo ORDER BY id_prestamo DESC LIMIT :lim")
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def obtener_prestamo(id_prestamo):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT * FROM prestamo WHERE id_prestamo = :id LIMIT 1")
        r = conn.execute(q, {"id": id_prestamo}).mappings().first()
        return dict(r) if r else None

