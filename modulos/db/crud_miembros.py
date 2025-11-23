# modulos/db/crud_miembros.py
from typing import Optional, List, Dict, Any
from sqlalchemy import text
from modulos.config.conexion import get_engine

# --------- Lectura / búsqueda ----------

def get_member_by_id(member_id: int) -> Optional[Dict[str, Any]]:
    """Devuelve un miembro por su id o None."""
    engine = get_engine()
    with engine.connect() as conn:
        q = text("""
            SELECT id_miembro, id_tipo_usuario, nombre, apellido, dui, direccion, correo,
                   telefono, fecha_nacimiento, estado
            FROM miembro
            WHERE id_miembro = :id
            LIMIT 1
        """)
        r = conn.execute(q, {"id": member_id}).mappings().first()
        return dict(r) if r else None

def get_member_by_dui(dui: str) -> Optional[Dict[str, Any]]:
    """Buscar miembro por DUI (único)."""
    engine = get_engine()
    with engine.connect() as conn:
        q = text("""
            SELECT id_miembro, id_tipo_usuario, nombre, apellido, dui, direccion, correo,
                   telefono, fecha_nacimiento, estado
            FROM miembro
            WHERE dui = :dui
            LIMIT 1
        """)
        r = conn.execute(q, {"dui": dui}).mappings().first()
        return dict(r) if r else None

def list_members(limit: int = 200, offset: int = 0) -> List[Dict[str, Any]]:
    """Lista miembros paginada (limit/offset)."""
    engine = get_engine()
    with engine.connect() as conn:
        q = text("""
            SELECT id_miembro, id_tipo_usuario, nombre, apellido, dui, direccion, correo,
                   telefono, fecha_nacimiento, estado
            FROM miembro
            ORDER BY id_miembro DESC
            LIMIT :lim OFFSET :off
        """)
        rows = conn.execute(q, {"lim": limit, "off": offset}).mappings().all()
        return [dict(r) for r in rows]

def search_members(term: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Búsqueda simple por nombre, apellido o DUI (LIKE)."""
    engine = get_engine()
    like = f"%{term}%"
    with engine.connect() as conn:
        q = text("""
            SELECT id_miembro, id_tipo_usuario, nombre, apellido, dui, direccion, correo,
                   telefono, fecha_nacimiento, estado
            FROM miembro
            WHERE nombre LIKE :t OR apellido LIKE :t OR dui LIKE :t
            ORDER BY nombre ASC
            LIMIT :lim
        """)
        rows = conn.execute(q, {"t": like, "lim": limit}).mappings().all()
        return [dict(r) for r in rows]

# --------- Creación / actualización / borrado ----------

def create_member(
    id_tipo_usuario: Optional[int],
    nombre: str,
    apellido: str,
    dui: Optional[str] = None,
    direccion: Optional[str] = None,
    correo: Optional[str] = None,
    telefono: Optional[str] = None,
    fecha_nacimiento: Optional[str] = None,  # usar formato 'YYYY-MM-DD' si aplica
    estado: str = "activo"
) -> Any:
    """
    Inserta un nuevo miembro. Devuelve lastrowid (si disponible) o True/False.
    """
    engine = get_engine()
    with engine.begin() as conn:
        q = text("""
            INSERT INTO miembro (
                id_tipo_usuario, nombre, apellido, dui, direccion, correo, telefono,
                fecha_nacimiento, estado
            ) VALUES (
                :id_tipo_usuario, :nombre, :apellido, :dui, :direccion, :correo, :telefono,
                :fecha_nacimiento, :estado
            )
        """)
        res = conn.execute(q, {
            "id_tipo_usuario": id_tipo_usuario,
            "nombre": nombre,
            "apellido": apellido,
            "dui": dui,
            "direccion": direccion,
            "correo": correo,
            "telefono": telefono,
            "fecha_nacimiento": fecha_nacimiento,
            "estado": estado
        })
        # intentar devolver id insertado si está disponible (MySQL connector)
        try:
            return res.lastrowid or True
        except Exception:
            return True

def update_member(member_id: int, **fields) -> bool:
    """
    Actualiza campos de un miembro. Pasar pares campo=valor.
    Devuelve True si afectó >=1 fila, False si no.
    """
    if not fields:
        return False
    allowed = {
        "id_tipo_usuario", "nombre", "apellido", "dui", "direccion", "correo",
        "telefono", "fecha_nacimiento", "estado"
    }
    # filtrar sólo columnas permitidas
    data = {k: v for k, v in fields.items() if k in allowed}
    if not data:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
    params = dict(data)
    params["id"] = member_id

    engine = get_engine()
    with engine.begin() as conn:
        q = text(f"UPDATE miembro SET {set_clause} WHERE id_miembro = :id")
        res = conn.execute(q, params)
        try:
            return res.rowcount and res.rowcount > 0
        except Exception:
            # algunos dialectos no presentan rowcount igual, devolver True por defecto
            return True

def delete_member(member_id: int) -> bool:
    """Elimina (o marca como inactivo según tu política)."""
    engine = get_engine()
    with engine.begin() as conn:
        q = text("DELETE FROM miembro WHERE id_miembro = :id")
        res = conn.execute(q, {"id": member_id})
        try:
            return res.rowcount and res.rowcount > 0
        except Exception:
            return True


