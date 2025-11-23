# modulos/config/conexion.py
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

_engine = None

def get_engine() -> Engine:
    global _engine
    if _engine is None:
        # usa DATABASE_URL o construye desde variables CLEVER
        db_url = os.getenv("DATABASE_URL") or os.getenv("MYSQL_ADDON_URI")
        if not db_url:
            # fallback: sqlite local (dev)
            db_url = "sqlite:///./data/gapc.db"
        _engine = create_engine(db_url, future=True)
    return _engine

