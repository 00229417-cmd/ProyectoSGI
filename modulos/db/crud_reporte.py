# modulos/db/crud_reporte.py
from modulos.config.conexion import get_engine
from sqlalchemy import text

def _resolve_administrador_id(maybe_id_or_text):
    """
    Si maybe_id_or_text es convertible a int lo devuelve.
    Si es texto, intenta buscar en la tabla administrador por nombre o correo.
    Devuelve int o None.
    """
    if maybe_id_or_text is None or maybe_id_or_text == "":
        return None

    # 1) intentar entero
    try:
        return int(maybe_id_or_text)
    except Exception:
        pass

    engine = get_engine()
    q = text("""
        SELECT id_administrador
        FROM administrador
        WHERE nombre = :val
           OR apellido = :val
           OR correo = :val
        LIMIT 1
    """)
    with engine.connect() as conn:
        r = conn.execute(q, {"val": maybe_id_or_text}).mappings().first()
        if r:
            return int(r["id_administrador"])
    return None

def create_reporte(id_ciclo, id_administrador, tipo, descripcion=None):
    """
    Inserta un reporte.
    id_ciclo: None o int (si se pasa texto se intenta convertir)
    id_administrador: int o texto (se intenta resolver)
    Devuelve (True, None) o (False, "mensaje")
    """
    engine = get_engine()

    # resolver administrador
    adm_id = _resolve_administrador_id(id_administrador)
    if adm_id is None:
        return False, "No se pudo resolver id_administrador válido. Pasa un ID numérico o el nombre/correo exacto."

    # resolver ciclo
    ciclo_val = None
    if id_ciclo is not None and id_ciclo != "":
        try:
            ciclo_val = int(id_ciclo)
        except Exception:
            return False, "id_ciclo debe ser numérico o vacío."

    q = text("""
        INSERT INTO reporte (id_ciclo, id_administrador, tipo, fecha_generacion, descripcion, estado)
        VALUES (:id_ciclo, :id_adm, :tipo, NOW(), :desc, 'pendiente')
    """)
    params = {"id_ciclo": ciclo_val, "id_adm": adm_id, "tipo": tipo, "desc": descripcion}
    try:
        with engine.begin() as conn:
            conn.execute(q, params)
        return True, None
    except Exception as e:
        return False, str(e)

