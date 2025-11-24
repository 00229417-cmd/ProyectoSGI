# modulos/db/crud_reporte.py
from modulos.config.conexion import get_engine
from sqlalchemy import text

def create_reporte(id_ciclo, id_administrador, tipo, descripcion=None):
    """
    Inserta un registro en la tabla `reporte`.
    Devuelve (True, None) si OK, o (False, "mensaje") si falla.
    """
    # validaciones mínimas
    try:
        id_adm_int = int(id_administrador)
    except Exception:
        return False, "id_administrador debe ser numérico."

    # id_ciclo puede ser None o int
    id_ciclo_val = None
    if id_ciclo is not None and id_ciclo != "":
        try:
            id_ciclo_val = int(id_ciclo)
        except Exception:
            return False, "id_ciclo debe ser numérico o vacío."

    engine = get_engine()
    q = text("""
        INSERT INTO reporte (id_ciclo, id_administrador, tipo, fecha_generacion, descripcion, estado)
        VALUES (:id_ciclo, :id_adm, :tipo, NOW(), :desc, 'pendiente')
    """)

    params = {"id_ciclo": id_ciclo_val, "id_adm": id_adm_int, "tipo": tipo, "desc": descripcion}

    try:
        with engine.begin() as conn:
            conn.execute(q, params)
        return True, None
    except Exception as e:
        return False, str(e)

