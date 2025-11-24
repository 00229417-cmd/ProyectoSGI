# modulos/db/crud_prestamo.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from datetime import datetime, date

def create_prestamo(id_ciclo, id_miembro, monto, intereses, plazo_meses, id_promotora=None, fecha_solicitud=None):
    """
    Crea un préstamo. fecha_solicitud puede ser:
      - None  -> se inserta NULL
      - datetime.date / datetime.datetime -> se usa directamente
      - string 'YYYY-MM-DD' o 'YYYY-MM-DD HH:MM:SS' -> se usa tal cual
    Retorna id del nuevo prestamo.
    """
    engine = get_engine()
    if fecha_solicitud is None:
        # si quieres que siempre tenga fecha, descomenta la siguiente línea:
        # fecha_solicitud = datetime.now()
        fecha_solicitud_val = None
    else:
        fecha_solicitud_val = fecha_solicitud

    sql = """
    INSERT INTO prestamo
      (id_promotora, id_ciclo, id_miembro, monto, intereses, saldo_restante, estado, plazo_meses, total_cuotas, fecha_solicitud)
    VALUES
      (:id_prom, :id_ciclo, :id_miembro, :monto, :intereses, :saldo, :estado, :plazo, :total_cuotas, :fecha_solicitud)
    """
    params = {
        "id_prom": id_promotora,
        "id_ciclo": id_ciclo,
        "id_miembro": id_miembro,
        "monto": monto,
        "intereses": intereses,
        "saldo": monto,
        "estado": "activo",
        "plazo": plazo_meses,
        "total_cuotas": 0,
        "fecha_solicitud": fecha_solicitud_val
    }
    try:
        with engine.begin() as conn:
            res = conn.execute(text(sql), params)
            # Respuesta depende del driver; si no hay lastrowid, puedes SELECT MAX(id_prestamo)
            try:
                return res.lastrowid
            except Exception:
                r = conn.execute(text("SELECT LAST_INSERT_ID() as id")).fetchone()
                return r["id"] if r else None
    except Exception as e:
        # lanza para que la página muestre el error real
        raise RuntimeError(f"Error creando prestamo: {e}")

