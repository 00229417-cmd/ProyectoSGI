# modulos/config/conexion.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

def get_database_url_from_env():
    """
    Lee la URI desde MYSQL_ADDON_URI o DATABASE_URL.
    Si solo hay host/user/password/db construye la URI.
    Convierte mysql:// -> mysql+pymysql:// para SQLAlchemy + PyMySQL.
    """
    uri = os.getenv("MYSQL_ADDON_URI") or os.getenv("DATABASE_URL")
    if uri:
        # soportar uri de la forma mysql://user:pass@host:port/db
        if uri.startswith("mysql://"):
            uri = uri.replace("mysql://", "mysql+pymysql://", 1)
        return uri

    host = os.getenv("MYSQL_ADDON_HOST")
    port = os.getenv("MYSQL_ADDON_PORT", "3306")
    db = os.getenv("MYSQL_ADDON_DB")
    user = os.getenv("MYSQL_ADDON_USER")
    password = os.getenv("MYSQL_ADDON_PASSWORD")
    if not all([host, db, user, password]):
        # no hay suficientes variables
        return None
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"

# motor singleton
_ENGINE = None

def get_engine(echo: bool = False):
    """
    Devuelve un engine SQLAlchemy (singleton).
    Lanza RuntimeError si no hay configuración de BD.
    """
    global _ENGINE
    if _ENGINE is None:
        DATABASE_URL = get_database_url_from_env()
        if not DATABASE_URL:
            raise RuntimeError("No se encontró configuración de BD en variables de entorno.")
        # create_engine acepta la URI con driver pymysql (mysql+pymysql://)
        _ENGINE = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600, echo=echo)
    return _ENGINE

def test_connection():
    """
    Ejecuta un SELECT 1 y retorna (True, mensaje) o (False, mensaje de error).
    Usa text(...) para evitar "Not an executable object".
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            r = result.scalar()
            return True, f"Conexión OK (SELECT 1 -> {r})"
    except OperationalError as e:
        return False, f"Error de conexión: {e}"
    except RuntimeError as e:
        return False, f"Configuración BD faltante: {e}"
    except Exception as e:
        return False, f"Error inesperado: {e}"
