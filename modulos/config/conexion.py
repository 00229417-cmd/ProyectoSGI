# modulos/config/conexion.py
"""
Conexión a la base de datos (MySQL / Clever Cloud).
Contiene funciones compatibles con versiones previas:
 - get_engine()    <- alias compatible (devuelve SQLAlchemy Engine)
 - test_connection() <- prueba de conexión simple (True or (False, error_msg))

Además expone:
 - create_engine_from_env()  <-- crea engine a partir de env vars / DATABASE_URL
 - get_connection()          <-- devuelve conexión (context manager)
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import quote_plus

# Tiempo de espera / argumentos por defecto para MySQL driver connector
DEFAULT_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    # puedes añadir más opciones si lo requieres
}

def create_engine_from_env() -> Engine:
    """
    Crea un SQLAlchemy engine según variables de entorno.
    Prioridad:
      1) DATABASE_URL (si está en formato SQLAlchemy: mysql+mysqlconnector://user:pass@host:port/db)
      2) MYSQL_ADDON_* (Clever Cloud style) -> se forma la URI
    """
    database_url = os.environ.get("DATABASE_URL") or os.environ.get("MYSQL_ADDON_URI")
    if database_url:
        # si viene con caracteres especiales en password y no está encodeado, puede fallar;
        # asumimos que la URI ya es correcta (como la que provee Clever Cloud).
        engine = create_engine(database_url, **DEFAULT_ENGINE_OPTIONS)
        return engine

    # Si no hay DATABASE_URL, intentamos montar desde MYSQL_ADDON_*
    host = os.environ.get("MYSQL_ADDON_HOST")
    port = os.environ.get("MYSQL_ADDON_PORT", "3306")
    db = os.environ.get("MYSQL_ADDON_DB")
    user = os.environ.get("MYSQL_ADDON_USER")
    password = os.environ.get("MYSQL_ADDON_PASSWORD")

    if host and db and user:
        # encode password safely
        pwd_enc = quote_plus(password) if password else ""
        uri = f"mysql+mysqlconnector://{user}:{pwd_enc}@{host}:{port}/{db}"
        engine = create_engine(uri, **DEFAULT_ENGINE_OPTIONS)
        return engine

    # Fallback: intenta SQLite local (útil para desarrollo rápido si nadie configuró env)
    fallback_sqlite = os.environ.get("FALLBACK_SQLITE", "data/gapc_dev.db")
    uri = f"sqlite:///{fallback_sqlite}"
    engine = create_engine(uri, connect_args={"check_same_thread": False}, **{"pool_pre_ping": True})
    return engine

# ---------------------
# Funciones públicas recomendadas
# ---------------------

def get_engine() -> Engine:
    """
    Alias de compatibilidad (esperado por varias partes del código).
    Devuelve SQLAlchemy Engine.
    """
    return create_engine_from_env()

def get_connection():
    """
    Context manager para obtener una conexión (usar con 'with').
    Ejemplo:
        with get_connection() as conn:
            conn.execute(text("SELECT 1"))
    """
    engine = get_engine()
    return engine.connect()

def test_connection():
    """
    Prueba rápida de conexión.
    Devuelve:
      - (True, None) si OK
      - (False, "mensaje de error") si falla
    Nota: hay partes del código que esperan simplemente True/False; para compatibilidad
    se devuelve una tupla (bool, message). Si prefieres True/False, cambia llamada en app.
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            # consulta simple validada por el motor
            conn.execute(text("SELECT 1"))
        return True, None
    except SQLAlchemyError as e:
        # devuelve False y el mensaje (sencillo)
        return False, str(e)
    except Exception as e:
        return False, str(e)

# ---------------------
# Helper util (opcional)
# ---------------------
def connection_info():
    """
    Información útil para debug (no incluir credenciales en logs públicos).
    """
    try:
        eng = get_engine()
        return {
            "dialect": str(eng.dialect.name),
            "pool": str(type(eng.pool))
        }
    except Exception:
        return {"error": "no engine"}

# Fin de archivo

