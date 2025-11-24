
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
    Crea un prestamo y retorna el id (id_prestamo) insertado.
    - fecha_solicitud: string 'YYYY-MM-DD' o 'YYYY-MM-DD HH:MM:SS' o None
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
        "saldo": float(monto),          # al crear, saldo_restante = monto inicialmente
        "estado": "activo",
        "plazo": int(plazo_meses),
        "total_cuotas": 0,
        "fecha_solicitud": fecha_solicitud
    }

    try:
        with engine.begin() as conn:
            res = conn.execute(text(sql), params)
            # Intentar devolver last insert id
            try:
                last = res.lastrowid
                return int(last) if last is not None else None
            except Exception:
                r = conn.execute(text("SELECT LAST_INSERT_ID() AS id")).fetchone()
                if r and ("id" in r or 0 in r):
                    return int(r["id"]) if "id" in r else int(r[0])
                return None
    except Exception as e:
        # no ocultes el error: sube la excepción para que la página lo muestre
        raise RuntimeError(f"Error creando prestamo: {e}")

def listar_prestamos(limit: int = 200):
    """
    Retorna lista de prestamos (rows) — útil para mostrar en la UI.
    """
    engine = get_engine()
    sql = "SELECT * FROM prestamo ORDER BY id_prestamo DESC LIMIT :lim"
    with engine.connect() as conn:
        rows = conn.execute(text(sql), {"lim": limit}).fetchall()
    return [dict(r) for r in rows]
