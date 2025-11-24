# modulos/db/crud_miembros.py
from sqlalchemy import text
from modulos.config.conexion import get_engine

# Guardamos engine en módulo para reusar
_engine = None

def _ensure_engine():
    global _engine
    if _engine is None:
        _engine = get_engine()
    return _engine

def list_miembros(limit: int = 500):
    """
    Retorna lista de miembros como lista de dicts.
    Usamos .mappings() para obtener filas como mapeos (clave->valor),
    compatible con diferentes versiones de SQLAlchemy.
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
        # RES: Result
        try:
            mappings = res.mappings().all()  # lista de MappingResult (dict-like)
            rows = [dict(r) for r in mappings]
        except Exception:
            # Fallback: intentar convertir cada row usando _mapping o enumerar columnas
            rows = []
            cols = res.keys()
            for r in res:
                try:
                    rows.append(dict(r._mapping))
                except Exception:
                    # último recurso: construir dict por posición usando columnas
                    rows.append({cols[i]: r[i] for i in range(len(cols))})
    return rows

def create_miembro(nombre: str, apellido: str, dui: str = None, direccion: str = None, id_tipo_usuario: int = None):
    """
    Inserta un miembro y retorna el id insertado.
    Usa INSERT + LAST_INSERT_ID() como fallback si res.lastrowid no está disponible.
    """
    engine = _ensure_engine()
    insert_sql = text("""
        INSERT INTO miembro (id_tipo_usuario, nombre, apellido, dui, direccion)
        VALUES (:id_tipo_usuario, :nombre, :apellido, :dui, :direccion)
    """)
    with engine.begin() as conn:
        res = conn.execute(insert_sql, {
            "id_tipo_usuario": id_tipo_usuario,
            "nombre": nombre,
            "apellido": apellido,
            "dui": dui,
            "direccion": direccion
        })
        # intentamos obtener lastrowid
        new_id = None
        try:
            new_id = int(res.lastrowid)
        except Exception:
            try:
                r = conn.execute(text("SELECT LAST_INSERT_ID() AS id")).fetchone()
                new_id = int(r["id"]) if r and "id" in r else None
            except Exception:
                new_id = None
    return new_id



