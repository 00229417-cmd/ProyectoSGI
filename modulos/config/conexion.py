# modulos/config/conexion.py
"""
Conexión a la base de datos (MySQL / Clever Cloud).
Versión mixta:
 - test_connection() -> bool
 - test_connection_verbose() -> (bool, mensaje)
 - get_engine(), get_connection() disponibles (compatibilidad)
La función create_engine_from_env normaliza DATABASE_URL tipo "mysql://" a
"mysql+mysqlconnector://" para evitar errores cuando un driver no está instalado.
"""

import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

# Opciones por defecto para el engine
DEFAULT_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    # puedes añadir "pool_size": 5 si lo necesitas
}

def create_engine_from_env() -> Engine:
    """
    Construye un SQLAlchemy engine usando variables de entorno:
      1) DATABASE_URL (normaliza mysql:// -> mysql+mysqlconnector://)
      2) MYSQL_ADDON_* (Clever Cloud style)
      3) fallback SQLite local (dev)
    """
    database_url = os.environ.get("DATABASE_URL") or os.environ.get("MYSQL_ADDON_URI")
    if database_url:
        # --- Normalizar si viene como mysql:// (sin especificador de driver)
        if database_url.startswith("mysql://"):
            # forzamos mysqlconnector (si prefieres pymysql, cambia aquí)
            database_url = database_url.replace("mysql://", "mysql+mysqlconnector://", 1)
        engine = create_engine(database_url, **DEFAULT_ENGINE_OPTIONS)
        return engine

    # Si no hay DATABASE_URL, intentamos montar desde MYSQL_ADDON_*
    host = os.environ.get("MYSQL_ADDON_HOST")
    port = os.environ.get("MYSQL_ADDON_PORT", "3306")
    db = os.environ.get("MYSQL_ADDON_DB")
    user = os.environ.get("MYSQL_ADDON_USER")
    password = os.environ.get("MYSQL_ADDON_PASSWORD")

    if host and db and user:
        pwd_enc = quote_plus(password) if password else ""
        uri = f"mysql+mysqlconnector://{user}:{pwd_enc}@{host}:{port}/{db}"
        engine = create_engine(uri, **DEFAULT_ENGINE_OPTIONS)
        return engine

    # Fallback a SQLite local (útil para desarrollo si no hay env)
    fallback_sqlite = os.environ.get("FALLBACK_SQLITE", "data/gapc_dev.db")
    uri = f"sqlite:///{fallback_sqlite}"
    engine = create_engine(uri, connect_args={"check_same_thread": False}, **{"pool_pre_ping": True})
    return engine

# ---------------------
# API pública
# ---------------------

def get_engine() -> Engine:
    """Alias: devuelve SQLAlchemy engine."""
    return create_engine_from_env()

def get_connection():
    """Devuelve una conexión (usar con 'with'). Ejemplo:
       with get_connection() as conn:
           conn.execute(text("SELECT 1"))
    """
    engine = get_engine()
    return engine.connect()

def test_connection() -> bool:
    """
    Prueba simple de conexión. Devuelve True si la conexión funciona, False si no.
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False

def test_connection_verbose():
    """
    Prueba de conexión con detalle.
    Devuelve (True, None) si OK, o (False, "mensaje") si falla.
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, None
    except SQLAlchemyError as e:
        # tratamos de sacar mensaje legible
        return False, str(e.__dict__.get("orig") or e)
    except Exception as e:
        return False, str(e)

def connection_info():
    """Información simple del engine (sin credenciales)."""
    try:
        eng = get_engine()
        return {"dialect": str(eng.dialect.name), "pool": str(type(eng.pool))}
    except Exception:
        return {"error": "no engine"}


