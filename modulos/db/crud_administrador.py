# modulos/db/crud_administrador.py
from modulos.config.conexion import get_engine
from sqlalchemy import text

def get_by_username_or_email(identifier: str):
    """
    Busca un administrador por:
      - id numérico (si se pasa como string convertible)
      - correo exacto
      - username exacto (si tienes username)
      - nombre completo "Nombre Apellido"
    Retorna dict con keys: id_administrador, nombre, apellido, correo, ... o None
    """
    if not identifier:
        return None

    engine = get_engine()

    # Si nos pasan un número como string, intentar buscar por id directamente
    try:
        iid = int(identifier)
        q = text("SELECT * FROM administrador WHERE id_administrador = :iid LIMIT 1")
        with engine.connect() as conn:
            r = conn.execute(q, {"iid": iid}).mappings().fetchone()
        return dict(r) if r else None
    except Exception:
        pass

    # Buscar por correo o por nombre/apellido (ajusta columnas si las tienes distintas)
    q = text("""
        SELECT * FROM administrador
        WHERE correo = :ident
           OR nombre = :ident
           OR apellido = :ident
           OR CONCAT(nombre, ' ', apellido) = :ident
        LIMIT 1
    """)
    with engine.connect() as conn:
        r = conn.execute(q, {"ident": identifier}).mappings().fetchone()
    return dict(r) if r else None
