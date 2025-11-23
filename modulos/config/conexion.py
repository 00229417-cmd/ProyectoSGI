# modulos/config/conexion.py
"""
Conexión robusta para MySQL / Clever Cloud.
Normaliza URIs que lleguen como "mysql://" a "mysql+mysqlconnector://"
y evita que SQLAlchemy intente importar MySQLdb (mysqlclient) no instalado.
"""

import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from typing import Tuple

# opciones seguras para engine
DEFAULT_ENGINE_OPTS = {
    "pool_pre_ping": True,
    "pool_recycle": 1800,
    # no incluir connect_args que rompan en algunos hosts por defecto
}

def _normalize_mysql_uri(uri: str) -> str:
    """
    Si la URI empieza por 'mysql://' la normalizamos a 'mysql+mysqlconnector://'
    para forzar el uso de mysql-connector-python (evita import MySQLdb).
    """
    if uri.startswith("mysql://"):
        return uri.replace("mysql://", "mysql+mysqlconnector://", 1)
    # si ya viene con driver explícito (mysql+...), la devolvemos tal cual
    return uri

def create_engine_from_env() -> Engine:
    """
    Construye un SQLAlchemy engine:
      - Prioridad 1: MYSQL_ADDON_URI o DATABASE_URL (si existe)
      - Prioridad 2: montar desde MYSQL_ADDON_HOST/USER/DB/PASSWORD
      - Si no hay suficientes vars, lanza RuntimeError.
    """
    # 1) URI completa (Clever Cloud suele proveer MYSQL_ADDON_URI)
    raw_uri = os.environ.get("MYSQL_ADDON_URI") or os.environ.get("DATABASE_URL") or os.environ.get("MYSQL_URL")
    if raw_uri:
        uri = _normalize_mysql_uri(raw_uri.strip())
        # Si la URI incluye contraseña con caracteres especiales, asumimos que ya viene urlencoded.
        return create_engine(uri, **DEFAULT_ENGINE_OPTS)

    # 2) Construir desde piezas
    host = os.environ.get("MYSQL_ADDON_HOST") or os.environ.get("DB_HOST")
    port = os.environ.get("MYSQL_ADDON_PORT") or os.environ.get("DB_PORT") or "3306"
    db = os.environ.get("MYSQL_ADDON_DB") or os.environ.get("DB_NAME")
    user = os.environ.get("MYSQL_ADDON_USER") or os.environ.get("DB_USER")
    password = os.environ.get("MYSQL_ADDON_PASSWORD") or os.environ.get("DB_PASSWORD")

    if host and db and user:
        pwd_enc = quote_plus(password) if password else ""
        uri = f"mysql+mysqlconnector://{user}:{pwd_enc}@{host}:{port}/{db}"
        return create_engine(uri, **DEFAULT_ENGINE_OPTS)

    # 3) Fallback: sqlite local (solo para desarrollo)
    fallback = os.environ.get("FALLBACK_SQLITE", "data/gapc_dev.db")
    sqlite_uri = f"sqlite:///{fallback}"
    return create_engine(sqlite_uri, connect_args={"check_same_thread": False})

# Engine en caché
_ENGINE: Engine | None = None

def get_engine() -> Engine:
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = create_engine_from_env()
    return _ENGINE

def test_connection() -> Tuple[bool, str]:
    """
    Prueba simple de conexión: devuelve (True, "") si OK, o (False, "mensaje") si falla.
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, ""
    except Exception as e:
        return False, str(e)

