# modulos/db/crud_cierre.py
from sqlalchemy import text
from modulos.config.conexion import get_engine

# -----------------------
# Helpers para ciclos
# -----------------------
def get_ciclo_by_id(id_ciclo):
    engine = get_engine()
    q = text("SELECT id_ciclo, fecha_inicio, fecha_fin, estado FROM ciclo WHERE id_ciclo = :id LIMIT 1")
    with engine.connect() as conn:
        r = conn.execute(q, {"id": id_ciclo}).mappings().first()
        return dict(r) if r else None

def get_latest_ciclo():
    engine = get_engine()
    q = text("SELECT id_ciclo, fecha_inicio, fecha_fin, estado FROM ciclo ORDER BY id_ciclo DESC LIMIT 1")
    with engine.connect() as conn:
        r = conn.execute(q).mappings().first()
        return dict(r) if r else None

def create_default_ciclo(fecha_inicio="1970-01-01", fecha_fin="2099-12-31", estado="abierto"):
    """
    Crea un ciclo por defecto y devuelve su id.
    """
    engine = get_engine()
    q_ins = text("""
        INSERT INTO ciclo (fecha_inicio, fecha_fin, estado, total_utilidad)
        VALUES (:fi, :ff, :est, 0)
    """)
    with engine.begin() as conn:
        res = conn.execute(q_ins, {"fi": fecha_inicio, "ff": fecha_fin, "est": estado})
        # obtener last inserted id (SQLAlchemy Core con engine)
        last_id = res.lastrowid
    return last_id

# -----------------------
# CRUD Cierre robusto
# -----------------------
def create_cierre(id_ciclo=None, resumen=""):
    """
    Inserta un cierre. Lógica:
    - Si id_ciclo provisto y existe -> usarlo.
    - Si id_ciclo provisto y NO existe -> tomar el último ciclo existente.
    - Si no existe NINGÚN ciclo -> crear uno por defecto y usarlo.
    Devuelve (ok:boolean, msg:str)
    """
    engine = get_engine()

    # 1) si nos dan id_ciclo, comprobar que exista
    if id_ciclo is not None:
        existing = get_ciclo_by_id(id_ciclo)
        if not existing:
            # intentar usar el ciclo último
            latest = get_latest_ciclo()
            if latest:
                id_ciclo = latest["id_ciclo"]
            else:
                # crear uno por defecto
                id_ciclo = create_default_ciclo()
    else:
        # si no se indicó id_ciclo, agarrar el último
        latest = get_latest_ciclo()
        if latest:
            id_ciclo = latest["id_ciclo"]
        else:
            id_ciclo = create_default_ciclo()

    q = text("INSERT INTO cierre (id_ciclo, fecha, resumen, estado) VALUES (:c, NOW(), :r, 'cerrado')")
    try:
        with engine.begin() as conn:
            conn.execute(q, {"c": id_ciclo, "r": resumen})
        return True, f"Cierre creado (id_ciclo={id_ciclo})"
    except Exception as e:
        return False, str(e)

# -----------------------
# Listar cierres (útil en la UI)
# -----------------------
def list_cierres(limit=200):
    engine = get_engine()
    q = text("SELECT id_cierre, id_ciclo, fecha, resumen, estado FROM cierre ORDER BY id_cierre DESC LIMIT :lim")
    with engine.connect() as conn:
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]
