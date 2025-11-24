# modulos/pages/miembros_page.py
import streamlit as st
from sqlalchemy import text
from modulos.config.conexion import get_engine

# Intentamos usar funciones CRUD si existen (mejor práctica)
try:
    from modulos.db.crud_miembros import list_members, create_member
except Exception:
    list_members = None
    create_member = None

def _fetch_members_from_db(limit=500):
    engine = get_engine()
    with engine.connect() as conn:
        q = text("SELECT id_miembro, id_tipo_usuario, nombre, apellido, dui, direccion FROM miembro ORDER BY id_miembro DESC LIMIT :lim")
        rows = conn.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in rows]

def _insert_member_direct(tipo_id, nombre, apellido, dui, direccion):
    engine = get_engine()
    with engine.begin() as conn:
        q = text("""
            INSERT INTO miembro (id_tipo_usuario, nombre, apellido, dui, direccion)
            VALUES (:tid, :nom, :ape, :dui, :dir)
        """)
        res = conn.execute(q, {"tid": tipo_id, "nom": nombre, "ape": apellido, "dui": dui, "dir": direccion})
        try:
            return res.lastrowid or True
        except Exception:
            return True

def miembros_page():
    st.header("Miembros")
    st.subheader("Lista de miembros registrados")

    # Mostrar lista
    members = []
    try:
        if list_members:
            members = list_members(limit=500)
        else:
            members = _fetch_members_from_db()
    except Exception as e:
        st.error(f"Error al obtener miembros: {e}")

    if not members:
        st.info("No hay miembros registrados todavía.")
    else:
        # convertir lista de dicts a tabla
        st.table(members)

    st.markdown("---")
    st.subheader("Registrar nuevo miembro")

    with st.form("form_nuevo_miembro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            tipo = st.number_input("ID tipo usuario (ej: 1)", min_value=1, step=1, value=1)
            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
        with col2:
            dui = st.text_input("DUI / identificación")
            direccion = st.text_area("Dirección", max_chars=250)
        submitted = st.form_submit_button("Crear miembro")

        if submitted:
            if not nombre or not apellido:
                st.error("Nombre y apellido son obligatorios.")
            else:
                try:
                    if create_member:
                        ok = create_member(tipo, nombre, apellido, dui, direccion)
                    else:
                        ok = _insert_member_direct(tipo, nombre, apellido, dui, direccion)
                    if ok:
                        st.success("Miembro creado correctamente.")
                        # recargar para actualizar la lista
                        try:
                            st.experimental_rerun()
                        except Exception:
                            pass
                    else:
                        st.error("No se pudo crear el miembro.")
                except Exception as ex:
                    st.error(f"Error al crear miembro: {ex}")


