# modulos/db/crud_miembros.py
from sqlalchemy import text
from modulos.config.conexion import get_engine
from datetime import datetime

# ---------- MIEMBROS ----------
# Asume una tabla `miembro` con columnas:
# id_miembro (PK autoinc), nombre, identificacion, telefono, direccion,
# fecha_afiliacion (DATE/DATETIME), estado

def crear_miembro(nombre: str, identificacion: str = None, telefono: str = None,
                  direccion: str = None, fecha_afiliacion: str = None, estado: str = "activo"):
    """
    Inserta un miembro en la tabla `miembro`.
    fecha_afiliacion: si None -> se usa current date.
    Devuelve lastrowid o True.
    """
    engine = get_engine()
    if not fecha_afiliacion:
        fecha_afiliacion = datetime.utcnow().strftime("%Y-%m-%d")
    with engine.begin() as conn:
        q = text("""
            INSERT INTO miembro (nombre, identificacion, telefono, direccion, fecha_afiliacion, estado)
            VALUES (:nombre, :ident, :tel, :dir, :fecha, :estado)
        """)
        res = conn.execute(q, {
            "nombre": nombre, "ident": identificacion,
            "tel": telefono, "dir": direccion,
            "fecha": fecha_afiliacion, "estado": estado
        })
        try:
            return res.lastrowid or True
        except Exception:
            return True

def obtener_miembro(id_miembro: int):
    """Retorna dict del miembro o None."""
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT * FROM miembro WHERE id_miembro = :id LIMIT 1")
        r = conn.execute(q, {"id": id_miembro}).mappings().first()
        return dict(r) if r else None

def listar_miembros(limit: int = 200, offset: int = 0):
    """Lista miembros (paginable con limit/offset)."""
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id_miembro, nombre, identificacion, telefono, direccion, fecha_afiliacion, estado FROM miembro ORDER BY id_miembro DESC LIMIT :lim OFFSET :off")
        rows = conn.execute(q, {"lim": limit, "off": offset}).mappings().all()
        return [dict(r) for r in rows]

def actualizar_miembro(id_miembro: int, nombre: str = None, identificacion: str = None,
                       telefono: str = None, direccion: str = None, estado: str = None):
    """Actualiza campos provistos del miembro. Devuelve True si se actualizó."""
    engine = get_engine()
    set_clauses = []
    params = {"id": id_miembro}
    if nombre is not None:
        set_clauses.append("nombre = :nombre"); params["nombre"] = nombre
    if identificacion is not None:
        set_clauses.append("identificacion = :ident"); params["ident"] = identificacion
    if telefono is not None:
        set_clauses.append("telefono = :tel"); params["tel"] = telefono
    if direccion is not None:
        set_clauses.append("direccion = :dir"); params["dir"] = direccion
    if estado is not None:
        set_clauses.append("estado = :estado"); params["estado"] = estado

    if not set_clauses:
        return False

    set_sql = ", ".join(set_clauses)
    with engine.begin() as conn:
        q = text(f"UPDATE miembro SET {set_sql} WHERE id_miembro = :id")
        res = conn.execute(q, params)
        return res.rowcount > 0

def eliminar_miembro(id_miembro: int):
    """Elimina (o marca) un miembro. Aquí hacemos delete físico."""
    engine = get_engine()
    with engine.begin() as conn:
        q = text("DELETE FROM miembro WHERE id_miembro = :id")
        res = conn.execute(q, {"id": id_miembro})
        return res.rowcount > 0

