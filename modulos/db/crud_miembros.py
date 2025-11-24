# modulos/db/crud_miembros.py
import pandas as pd
import sqlalchemy
import traceback
from modulos.config.conexion import get_engine

ENGINE = None

def _get_engine():
    global ENGINE
    if ENGINE is None:
        ENGINE = get_engine()
    return ENGINE

# -------------------------
# Lectura
# -------------------------
def list_members(limit: int = 500):
    """
    Devuelve un DataFrame con los miembros. Si falta alguna columna, captura el error
    y devuelve (None, mensaje_error).
    """
    engine = _get_engine()
    sql = "SELECT id_miembro, id_tipo_usuario, nombre, apellido, dui, direccion FROM miembro ORDER BY id_miembro DESC LIMIT :lim"
    try:
        with engine.connect() as conn:
            df = pd.read_sql(sql=sql, con=conn, params={"lim": limit})
        return df, None
    except Exception as e:
        # retornar None y el mensaje para que la UI lo muestre sin romper
        return None, f"Error al listar miembros: {e}"

# -------------------------
# Crear
# -------------------------
def create_member(nombre: str, apellido: str, dui: str = None, direccion: str = None, id_tipo_usuario: int = None):
    """
    Inserta un miembro. Devuelve (True, id_insertado) o (False, mensaje_error).
    No modifica el esquema; si alguna columna no existe, captura y devuelve el error.
    """
    engine = _get_engine()
    # Insert usar columnas que normalmente existen en tu esquema
    sql = """
    INSERT INTO miembro (id_tipo_usuario, nombre, apellido, dui, direccion)
    VALUES (:id_tipo_usuario, :nombre, :apellido, :dui, :direccion)
    """
    try:
        with engine.begin() as conn:
            res = conn.execute(sqlalchemy.text(sql), {
                "id_tipo_usuario": id_tipo_usuario,
                "nombre": nombre,
                "apellido": apellido,
                "dui": dui,
                "direccion": direccion
            })
            # obtener id insertado si es posible
            try:
                inserted_id = res.lastrowid
            except Exception:
                inserted_id = None
        return True, inserted_id
    except Exception as e:
        tb = traceback.format_exc()
        return False, f"Error creando miembro: {e}\n{tb}"

# -------------------------
# Actualizar
# -------------------------
def update_member(id_miembro: int, nombre: str = None, apellido: str = None, dui: str = None, direccion: str = None, id_tipo_usuario: int = None):
    """
    Actualiza campos del miembro (solo los enviados no None).
    """
    engine = _get_engine()
    fields = {}
    if id_tipo_usuario is not None:
        fields["id_tipo_usuario"] = id_tipo_usuario
    if nombre is not None:
        fields["nombre"] = nombre
    if apellido is not None:
        fields["apellido"] = apellido
    if dui is not None:
        fields["dui"] = dui
    if direccion is not None:
        fields["direccion"] = direccion

    if not fields:
        return False, "Nada para actualizar."

    set_clause = ", ".join([f"{k} = :{k}" for k in fields.keys()])
    sql = f"UPDATE miembro SET {set_clause} WHERE id_miembro = :id_miembro"
    params = fields.copy()
    params["id_miembro"] = id_miembro

    try:
        with engine.begin() as conn:
            res = conn.execute(sqlalchemy.text(sql), params)
            return True, res.rowcount
    except Exception as e:
        tb = traceback.format_exc()
        return False, f"Error actualizando miembro: {e}\n{tb}"

# -------------------------
# Borrar
# -------------------------
def delete_member(id_miembro: int):
    """
    Elimina un miembro por id. Devuelve (True, rows_deleted) o (False, mensaje_error).
    """
    engine = _get_engine()
    sql = "DELETE FROM miembro WHERE id_miembro = :id_miembro"
    try:
        with engine.begin() as conn:
            res = conn.execute(sqlalchemy.text(sql), {"id_miembro": id_miembro})
            return True, res.rowcount
    except Exception as e:
        tb = traceback.format_exc()
        return False, f"Error eliminando miembro: {e}\n{tb}"


