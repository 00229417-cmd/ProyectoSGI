# modulos/db/crud_reporte.py (ejemplo)
from modulos.config.conexion import get_engine
from sqlalchemy import text

def create_reporte(id_ciclo, id_administrador, tipo, descripcion):
    """
    Crea un registro en la tabla reporte.
    Devuelve (True, "") si OK, o (False, "mensaje") si falla.
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            q = text("""
                INSERT INTO reporte (id_ciclo, id_administrador, tipo, fecha_generacion, descripcion, estado)
                VALUES (:id_ciclo, :id_adm, :tipo, NOW(), :desc, 'pendiente')
            """)
            params = {"id_ciclo": id_ciclo, "id_adm": id_administrador, "tipo": tipo, "desc": descripcion}
            conn.execute(q, params)
            return True, ""
    except Exception as e:
        return False, str(e)

def list_reportes(limit=200):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id_reporte, id_ciclo, id_administrador, tipo, fecha_generacion, descripcion, estado FROM reporte ORDER BY id_reporte DESC LIMIT :lim")
        res = conn.execute(q, {"lim": limit}).mappings().all()
        # devolver lista de dicts
        return [dict(r) for r in res]

