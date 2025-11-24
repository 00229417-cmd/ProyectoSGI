# modulos/db/crud_miembros.py
from sqlalchemy import text
from modulos.config.conexion import get_engine

# Números simples: devuelve engine (debe estar definido en modulos.config.conexion)
_engine = None

def _ensure_engine():
    global _engine
    if _engine is None:
        _engine = get_engine()
    return _engine

def list_miembros(limit: int = 500):
    """
    Retorna lista de miembros como lista de dicts.
    Intenta seleccionar columnas básicas que mencionaste.
    """
    engine = _ensure_engine()
    sql = text("""
        SELECT
            id_miembro,
            id_tipo_usuario,
            nombre,
            apellido,
            dui,
            direccion
        FROM miembro
        ORDER BY id_miembro DESC
        LIMIT :lim
    """)
    with engine.connect() as conn:
        res = conn.execute(sql, {"lim": limit})
        rows = [dict(r) for r in res.fetchall()]
    return rows

def create_miembro(nombre: str, apellido: str, dui: str = None, direccion: str = None, id_tipo_usuario: int = None):
    """
    Inserta un miembro y retorna el id insertado.
    Usa INSERT + SELECT LAST_INSERT_ID() (compatible MySQL/MariaDB).
    """
    engine = _ensure_engine()
    insert_sql = text("""
        INSERT INTO miembro (id_tipo_usuario, nombre, apellido, dui, direccion)
        VALUES (:id_tipo_usuario, :nombre, :apellido, :dui, :direccion)
    """)
    with engine.begin() as conn:  # begin() para commit automático
        res = conn.execute(insert_sql, {
            "id_tipo_usuario": id_tipo_usuario,
            "nombre": nombre,
            "apellido": apellido,
            "dui": dui,
            "direccion": direccion
        })
        # res.lastrowid funciona con SQLAlchemy/MySQL connectors
        try:
            new_id = res.lastrowid
        except Exception:
            # Fallback estándar SQL: SELECT LAST_INSERT_ID()
            last_sql = text("SELECT LAST_INSERT_ID() AS id")
            r = conn.execute(last_sql).fetchone()
            new_id = int(r["id"]) if r else None
    return new_id


