# modulos/config/conexion.py
# Conexión con SQLAlchemy (usa mysql+mysqlconnector). Lee variables de entorno.
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL

def get_database_url_from_env():
    """
    Prioriza DATABASE_URL, si no existe usa las vars MYSQL_ADDON_* (Clever Cloud).
    """
    db_url = os.environ.get("DATABASE_URL") or os.environ.get("DATABASE_URI") or os.environ.get("MYSQL_ADDON_URI")
    if db_url:
        return db_url

    host = os.environ.get("MYSQL_ADDON_HOST")
    port = os.environ.get("MYSQL_ADDON_PORT", "3306")
    user = os.environ.get("MYSQL_ADDON_USER")
    password = os.environ.get("MYSQL_ADDON_PASSWORD")
    dbname = os.environ.get("MYSQL_ADDON_DB")

    if host and user and password and dbname:
        return f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}"

    # fallback to sqlite local for dev (if none provided)
    local = os.environ.get("LOCAL_SQLITE_PATH", "sqlite:///data/gapc.db")
    return local

# create engine lazily
_ENGINE = None
def get_engine(echo=False):
    global _ENGINE
    if _ENGINE is None:
        url = get_database_url_from_env()
        _ENGINE = create_engine(url, echo=echo, future=True)
    return _ENGINE

def test_connection():
    """
    Devuelve (True, msg) si OK, (False, msg) si fallo.
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            r = conn.execute(text("SELECT 1"))
            # consume to ensure it runs
            _ = r.scalar()
        return True, "OK"
    except Exception as e:
        return False, str(e)
