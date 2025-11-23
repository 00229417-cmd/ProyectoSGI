# modulos/db/crud_users.py
from typing import Optional
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from modulos.config.conexion import get_engine

def create_user_and_member(
    username: str,
    password: str,
    full_name: Optional[str] = None,
    dni: Optional[str] = None,
    telefono: Optional[str] = None,
    direccion: Optional[str] = None,
    role: str = "user"
) -> Optional[int]:
    """
    Inserta usuario (con hash) y crea también el registro en la tabla `miembro`.
    Retorna user_id (int) si fue exitoso, None si hubo error.
    Ajusta nombres de columnas/table si tu ER difiere.
    """
    engine = get_engine()
    insert_user_sql = text("""
        INSERT INTO usuario (username, password_hash, full_name, role)
        VALUES (:username, :password_hash, :full_name, :role)
    """)

    # ajuste: nombre de la tabla miembro según tu ER; aquí se asume 'miembro' con campo id_usuario
    insert_miembro_sql = text("""
        INSERT INTO miembro (id_usuario, nombre, identificacion, telefono, direccion, fecha_afiliacion, estado)
        VALUES (:id_usuario, :nombre, :identificacion, :telefono, :direccion, CURRENT_DATE(), 'activo')
    """)

    password_hash = generate_password_hash(password)

    try:
        with engine.begin() as conn:
            # crear usuario
            res = conn.execute(insert_user_sql, {
                "username": username,
                "password_hash": password_hash,
                "full_name": full_name,
                "role": role
            })

            # Obtener id del usuario insertado de forma segura
            # (hacemos SELECT para compatibilidad con distintos drivers)
            sel = conn.execute(text("SELECT id FROM usuario WHERE username = :username LIMIT 1"), {"username": username})
            row = sel.fetchone()
            if not row:
                raise Exception("No se pudo obtener id del usuario insertado.")
            user_id = row[0]

            # crear miembro vinculado (si existe la tabla miembro)
            try:
                conn.execute(insert_miembro_sql, {
                    "id_usuario": user_id,
                    "nombre": full_name or username,
                    "identificacion": dni,
                    "telefono": telefono,
                    "direccion": direccion
                })
            except Exception:
                # Si la tabla miembro no existe o falla, no abortamos la transacción principal.
                # Podemos registrar/loggear y continuar. (Si prefieres que falle, lanza la excepción)
                pass

            return int(user_id)
    except SQLAlchemyError as e:
        print("create_user_and_member SQLAlchemyError:", e)
        return None
    except Exception as e:
        print("create_user_and_member error:", e)
        return None
