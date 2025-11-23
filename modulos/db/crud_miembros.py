# modulos/db/crud_users.py
from modulos.config.conexion import get_engine
from sqlalchemy import text

def create_user_and_member(username, password_hash, full_name, dni=None, telefono=None, direccion=None):
    engine = get_engine()
    with engine.begin() as conn:
        # inserta usuario
        res = conn.execute(text("INSERT INTO usuario (username, password_hash, full_name) VALUES (:u,:p,:f)"),
                           {"u":username, "p":password_hash, "f":full_name})
        user_id = res.lastrowid
        # inserta miembro (ajusta campos a tu ER)
        conn.execute(text("INSERT INTO miembro (id_usuario, nombre, identificacion, telefono, direccion, fecha_afiliacion, estado) VALUES (:uid, :nombre, :idn, :tel, :dir, CURRENT_DATE(), 'activo')"),
                     {"uid":user_id, "nombre":full_name, "idn":dni, "tel":telefono, "dir":direccion})
    return user_id
