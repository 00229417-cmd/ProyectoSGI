# modulos/db/crud_prestamo.py
from typing import Optional
from sqlalchemy import text
from modulos.config.conexion import get_engine

def create_prestamo(
    id_ciclo: int,
    id_miembro: int,
    monto: float,
    intereses: float,
    plazo_meses: int,
    id_promotora: Optional[int] = None,
    fecha_solicitud: Optional[str] = None
) -> Optional[int]:
    """
    Crea un préstamo y retorna el id insertado.
    """
    engine = get_engine()

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
        "monto": float(monto),
        "intereses": float(intereses),
        "saldo": float(monto),
        "estado": "activo",
        "plazo": int(plazo_meses),
        "total_cuotas": 0,
        "fecha_solicitud": fecha_solicitud
    }

    try:
        with engine.begin() as conn:
            res = conn.execute(text(sql), params)
            # Intentos robustos para obtener last insert id
            try:
                last = res.lastrowid
                if last:
                    return int(last)
            except Exception:
                pass
            # Fallback
            r = conn.execute(text("SELECT LAST_INSERT_ID() AS id")).mappings().first()
            if r and "id" in r:
                return int(r["id"])
            return None
    except Exception as e:
        raise RuntimeError(f"Error creando prestamo: {e}")


def listar_prestamos(limit: int = 200):
    """
    Retorna lista de prestamos (como lista de dicts).
    Usa .mappings() para obtener MappingResult (diccionarios).
    """
    engine = get_engine()
    sql = "SELECT * FROM prestamo ORDER BY id_prestamo DESC LIMIT :lim"
    try:
        with engine.connect() as conn:
            rows = conn.execute(text(sql), {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]
    except Exception as e:
        raise RuntimeError(f"Error listando préstamos: {e}")



