# modulos/config/conexion.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from typing import Tuple

DEFAULT_ENGINE_OPTS = {
    "pool_pre_ping": True,
    "pool_recycle": 1800,
    "connect_args": {"connect_timeout": 10},
}

def create_engine_from_env() -> Engine:
    """
    Construye engine desde MYSQL_ADDON_URI (preferido) o desde host/db/user/pass.
    Usa mysql+mysqlconnector (asegúrate de tener mysql-connector-python en requirements).
    """
    uri = os.environ.get("MYSQL_ADDON_URI") or os.environ.get("DATABASE_URL")
    if uri:
        # si la URI ya es válida para SQLAlchemy, úsala directamente
        return create_engine(uri, **DEFAULT_ENGINE_OPTS)
    # si no, armar desde piezas
    host = os.environ.get("MYSQL_ADDON_HOST")
    port = os.environ.get("MYSQL_ADDON_PORT", "3306")
    db = os.environ.get("MYSQL_ADDON_DB") or os.environ.get("MYSQL_DATABASE")
    user = os.environ.get("MYSQL_ADDON_USER") or os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_ADDON_PASSWORD") or os.environ.get("MYSQL_PASSWORD")
    if not all([host, db, user, password]):
        raise RuntimeError("Faltan variables de entorno para la conexión a la DB.")
    uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}"
    return create_engine(uri, **DEFAULT_ENGINE_OPTS)

# Engine único (lazy)
_ENGINE = None

def get_engine():
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = create_engine_from_env()
    return _ENGINE

def test_connection() -> Tuple[bool, str]:
    """
    Ejecuta SELECT 1 para probar la conexión.
    Devuelve (True, '') si OK, (False, mensaje) si falla.
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            # usar text() para compatibilidad
            r = conn.execute(text("SELECT 1")).scalar()
            if r is None:
                return False, "SELECT 1 returned no value"
        return True, ""
    except Exception as e:
        return False, str(e)


