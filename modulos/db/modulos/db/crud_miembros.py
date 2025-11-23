from sqlalchemy import text
from modulos.config.conexion import get_engine

def obtener_miembros(limit=100):
    engine = get_engine()
    with engine.connect() as conn:
        r = conn.execute(text("SELECT * FROM miembro LIMIT :lim"), {"lim": limit})
        return [dict(row) for row in r]

def crear_miembro(data):
    sql = text("""
        INSERT INTO miembro (id_tipo_usuario, nombre, apellido, dui, direccion)
        VALUES (:id_tipo_usuario, :nombre, :apellido, :dui, :direccion)
    """)
    engine = get_engine()
    with engine.begin() as conn:
        result = conn.execute(sql, data)
        return result.lastrowid
