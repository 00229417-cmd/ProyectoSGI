# modulos/db/crud_aporte.py
"""
CRUD sencillo para 'aporte'.
Se asume que existe `modulos.config.conexion.get_engine()` que devuelve un SQLAlchemy Engine.
Funciones:
 - list_aportes(limit=200)
 - get_aporte(id_aporte)
 - create_aporte(data_dict) -> id creado
 - update_aporte(id_aporte, data_dict)
 - delete_aporte(id_aporte)
"""

from typing import List, Dict, Optional
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from modulos.config.conexion import get_engine

def _execute_query(query: str, params: dict = None):
    engine = get_engine()
    with engine.connect() as conn:
        return conn.execute(text(query), params or {})

def list_aportes(limit: int = 200) -> List[Dict]:
    """
    Retorna lista de aportes como lista de diccionarios.
    Evita lanzar excepción si la tabla no existe — devuelve [] y registra en consola.
    """
    try:
        q = "SELECT id_aporte, id_miembro, id_reunion, monto, fecha, tipo FROM aporte ORDER BY id_aporte DESC LIMIT :lim"
        res = _execute_query(q, {"lim": limit})
        rows = [dict(r._mapping) for r in res]
        return rows
    except SQLAlchemyError as e:
        # log en consola (puedes reemplazar por logger)
        print("Error list_aportes:", e)
        return []

def get_aporte(id_aporte: int) -> Optional[Dict]:
    try:
        q = "SELECT * FROM aporte WHERE id_aporte = :id"
        res = _execute_query(q, {"id": id_aporte})
        row = res.fetchone()
        return dict(row._mapping) if row else None
    except SQLAlchemyError as e:
        print("Error get_aporte:", e)
        return None

def create_aporte(data: Dict) -> Optional[int]:
    """
    data espera keys: id_miembro, id_reunion (opcional), monto, fecha (YYYY-MM-DD), tipo
    Retorna id creado o None en error.
    """
    try:
        q = """
        INSERT INTO aporte (id_miembro, id_reunion, monto, fecha, tipo)
        VALUES (:id_miembro, :id_reunion, :monto, :fecha, :tipo)
        """
        res = _execute_query(q, {
            "id_miembro": data.get("id_miembro"),
            "id_reunion": data.get("id_reunion"),
            "monto": data.get("monto"),
            "fecha": data.get("fecha"),
            "tipo": data.get("tipo"),
        })
        # obtener lastrowid depende del driver; con SQLAlchemy core:
        engine = get_engine()
        with engine.connect() as conn:
            last = conn.execute(text("SELECT LAST_INSERT_ID() AS id")).fetchone()
            return int(last['id']) if last else None
    except SQLAlchemyError as e:
        print("Error create_aporte:", e)
        return None

def update_aporte(id_aporte: int, data: Dict) -> bool:
    try:
        q = """
        UPDATE aporte
        SET id_miembro = :id_miembro,
            id_reunion = :id_reunion,
            monto = :monto,
            fecha = :fecha,
            tipo = :tipo
        WHERE id_aporte = :id_aporte
        """
        _execute_query(q, {
            "id_miembro": data.get("id_miembro"),
            "id_reunion": data.get("id_reunion"),
            "monto": data.get("monto"),
            "fecha": data.get("fecha"),
            "tipo": data.get("tipo"),
            "id_aporte": id_aporte,
        })
        return True
    except SQLAlchemyError as e:
        print("Error update_aporte:", e)
        return False

def delete_aporte(id_aporte: int) -> bool:
    try:
        q = "DELETE FROM aporte WHERE id_aporte = :id"
        _execute_query(q, {"id": id_aporte})
        return True
    except SQLAlchemyError as e:
        print("Error delete_aporte:", e)
        return False


