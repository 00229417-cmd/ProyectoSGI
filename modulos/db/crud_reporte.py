# modulos/db/crud_reporte.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from typing import Optional, List, Dict, Any

def create_reporte(id_ciclo: int | str,
                   id_administrador_or_username: int | str,
                   tipo: str,
                   descripcion: Optional[str] = "") -> dict:
    """
    Crea un reporte. id_administrador_or_username puede ser:
      - un int (id_administrador)
      - o un username/email/nombre (str) -> se intentará resolver a id_administrador
    Devuelve dict con keys: ok (bool), msg (str), id (int|None)
    """
    engine = get_engine()
    with engine.connect() as conn:
        # resolver id_ciclo a entero
        try:
            id_ciclo_int = int(id_ciclo) if id_ciclo is not None and id_ciclo != "" else None
        except Exception:
            return {"ok": False, "msg": f"id_ciclo inválido: {id_ciclo}", "id": None}

        # resolver id_administrador
        id_adm = None
        try:
            id_adm = int(id_administrador_or_username)
        except Exception:
            # buscar por correo / nombre / username (ajusta columnas si tu tabla usa otra)
            q = text("SELECT id_administrador FROM administrador WHERE correo = :u OR nombre = :u LIMIT 1")
            r = conn.execute(q, {"u": id_administrador_or_username}).fetchone()
            if r:
                id_adm = int(r[0])

        if id_adm is None:
            return {"ok": False, "msg": f"No se encontró id_administrador para '{id_administrador_or_username}'", "id": None}

        # Insertar. si id_ciclo_int es None, insertar NULL (si tu columna lo permite)
        q_ins = text("""
            INSERT INTO reporte (id_ciclo, id_administrador, tipo, fecha_generacion, descripcion, estado)
            VALUES (:id_ciclo, :id_adm, :tipo, NOW(), :desc, 'pendiente')
        """)
        params = {"id_ciclo": id_ciclo_int, "id_adm": id_adm, "tipo": tipo, "desc": descripcion or ""}
        try:
            res = conn.execute(q_ins, params)
            # obtener id insertado si tu driver soporta lastrowid
            try:
                new_id = int(res.lastrowid)
            except Exception:
                new_id = None
            return {"ok": True, "msg": "Reporte creado", "id": new_id}
        except Exception as e:
            return {"ok": False, "msg": f"Error creando reporte: {e}", "id": None}


def list_reportes(limit: int = 200) -> List[Dict[str, Any]]:
    """
    Devuelve los últimos reportes (básico).
    """
    engine = get_engine()
    with engine.connect() as conn:
        q = text("""
            SELECT r.id_reporte, r.id_ciclo, r.id_administrador, a.nombre AS admin_nombre,
                   r.tipo, r.fecha_generacion, r.descripcion, r.estado
            FROM reporte r
            LEFT JOIN administrador a ON a.id_administrador = r.id_administrador
            ORDER BY r.id_reporte DESC
            LIMIT :lim
        """)
        rows = conn.execute(q, {"lim": limit}).fetchall()
        result = []
        for row in rows:
            result.append({
                "id_reporte": row[0],
                "id_ciclo": row[1],
                "id_administrador": row[2],
                "admin_nombre": row[3],
                "tipo": row[4],
                "fecha_generacion": row[5],
                "descripcion": row[6],
                "estado": row[7],
            })
        return result
