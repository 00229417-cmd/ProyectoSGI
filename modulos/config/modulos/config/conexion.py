import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

def get_database_url_from_env():
    uri = os.getenv("MYSQL_ADDON_URI") or os.getenv("DATABASE_URL")
    if uri:
        if uri.startswith("mysql://"):
            uri = uri.replace("mysql://", "mysql+pymysql://", 1)
        return uri
    host = os.getenv("MYSQL_ADDON_HOST")
    port = os.getenv("MYSQL_ADDON_PORT", "3306")
    db = os.getenv("MYSQL_ADDON_DB")
    user = os.getenv("MYSQL_ADDON_USER")
    password = os.getenv("MYSQL_ADDON_PASSWORD")
    if not all([host, db, user, password]):
        return None
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"

_ENGINE = None
def get_engine(echo: bool = False):
    global _ENGINE
    if _ENGINE is None:
        DATABASE_URL = get_database_url_from_env()
        if not DATABASE_URL:
            raise RuntimeError("No se encontró configuración de BD en variables de entorno.")
        _ENGINE = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600, echo=echo)
    return _ENGINE

def test_connection():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            r = conn.execute("SELECT 1").scalar()
            return True, f"Conexión OK (SELECT 1 -> {r})"
    except OperationalError as e:
        return False, f"Error de conexión: {e}"
    except Exception as e:
        return False, f"Error inesperado: {e}"
