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

    # Mostrar error si list_miembros no existe (captura y muestra con detalle)
    try:
        miembros = crud_miembros.list_miembros(limit=500)
    except Exception as e:
        st.error(f"Error cargando miembros: {e}")
        miembros = []

    # Tabla (pandas)
    if miembros:
        df = pd.DataFrame(miembros)
        # columnas ordenadas si existen
        cols_preferidas = ["id_miembro", "nombre", "apellido", "dui", "direccion", "id_tipo_usuario"]
        cols_final = [c for c in cols_preferidas if c in df.columns] + [c for c in df.columns if c not in cols_preferidas]
        st.subheader("Listado")
        st.dataframe(df[cols_final].reset_index(drop=True))
    else:
        st.subheader("Listado")
        st.info("No hay miembros registrados todavía.")

    st.markdown("---")

    # Formulario dentro de un expander (se despliega con botón)
    with st.expander("➕ Crear nuevo miembro", expanded=False):
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        dui = st.text_input("DUI (opcional)")
        direccion = st.text_input("Dirección (opcional)")
        id_tipo_usuario = st.number_input("ID Tipo usuario (opcional)", min_value=0, step=1, value=0)

        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Guardar miembro"):
                # Validaciones mínimas
                if not nombre.strip() or not apellido.strip():
                    st.error("Nombre y apellido son obligatorios.")
                else:
                    try:
                        # Si el usuario dejó 0 lo pasamos como None para la BD
                        tipo = None if id_tipo_usuario == 0 else int(id_tipo_usuario)
                        new_id = crud_miembros.create_miembro(nombre.strip(), apellido.strip(), dui.strip() or None, direccion.strip() or None, tipo)
                        st.success(f"Miembro creado correctamente. id = {new_id}.")
                        # recargar la página para mostrar el nuevo registro
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error guardando miembro: {e}")

    # Mensaje de ayuda / debugging opcional
    st.caption("Si ves errores, mira la consola de logs del servidor o pega aquí el traceback.")



