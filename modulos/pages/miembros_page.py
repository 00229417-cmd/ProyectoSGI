# modulos/pages/miembros_page.py
import streamlit as st
import pandas as pd
from modulos.db import crud_miembros
from modulos.config.conexion import test_connection

def render_miembros():
    st.markdown("### 👥 Miembros")

    # Conexión DB
    ok, msg = test_connection()
    if not ok:
        st.warning(f"DB: NO CONECTADO ({msg})")
    else:
        st.success("DB conectado")

    # Intentamos cargar miembros (capturamos excepciones y mostramos mensaje claro)
    miembros = []
    try:
        miembros = crud_miembros.list_miembros(limit=500)
        # Asegurarnos que sea una lista de dicts
        if isinstance(miembros, dict):
            # si por error recibimos dict, convertir a lista
            miembros = [miembros]
        if miembros is None:
            miembros = []
    except Exception as e:
        st.error(f"Error cargando miembros: {e}")
        miembros = []

    # Mostrar tabla
    st.subheader("Listado")
    if miembros:
        # Si viene como lista de tuplas u otra cosa convertimos con cuidado
        try:
            df = pd.DataFrame(miembros)
        except Exception:
            # Intento robusto: construir DF desde iteración
            records = []
            for item in miembros:
                if isinstance(item, dict):
                    records.append(item)
                else:
                    # intentar convertir item._mapping o atributos
                    try:
                        records.append(dict(item._mapping))
                    except Exception:
                        # como último recurso ignoramos
                        pass
            df = pd.DataFrame(records)

        if df.empty:
            st.info("No hay miembros para mostrar (tabla vacía).")
        else:
            cols_preferidas = ["id_miembro", "nombre", "apellido", "dui", "direccion", "id_tipo_usuario"]
            cols_final = [c for c in cols_preferidas if c in df.columns] + [c for c in df.columns if c not in cols_preferidas]
            st.dataframe(df[cols_final].reset_index(drop=True))
    else:
        st.info("No hay miembros registrados todavía.")

    st.markdown("---")

    # Formulario dentro de un expander (se despliega con botón)
    with st.expander("➕ Crear nuevo miembro", expanded=False):
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        dui = st.text_input("DUI (opcional)")
        direccion = st.text_input("Dirección (opcional)")
        id_tipo_usuario = st.number_input("ID Tipo usuario (opcional)", min_value=0, step=1, value=0)

        if st.button("Guardar miembro"):
            if not nombre.strip() or not apellido.strip():
                st.error("Nombre y apellido son obligatorios.")
            else:
                try:
                    tipo = None if id_tipo_usuario == 0 else int(id_tipo_usuario)
                    new_id = crud_miembros.create_miembro(
                        nombre.strip(), apellido.strip(),
                        dui.strip() or None, direccion.strip() or None, tipo
                    )
                    if new_id:
                        st.success(f"Miembro creado correctamente. id = {new_id}.")
                        # recargar la app para ver el nuevo registro
                        st.experimental_rerun()
                    else:
                        st.warning("Miembro insertado pero no se obtuvo id (posible driver). Refresca la página.")
                except Exception as e:
                    st.error(f"Error guardando miembro: {e}")

    st.caption("Si persiste un error pega aquí el traceback completo (o el mensaje de logs).")


