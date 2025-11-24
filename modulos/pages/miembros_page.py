# modulos/pages/miembros_page.py
import streamlit as st
from modulos.db.crud_miembros import (
    obtener_miembros,
    crear_miembro,
    actualizar_miembro,
    eliminar_miembro,
    obtener_tipos_usuario,
)

def render_miembros():
    st.header("👥 Gestión de Miembros")

    # --- Crear nuevo miembro (expander / formulario) ---
    with st.expander("➕ Crear nuevo miembro"):
        with st.form("form_crear_miembro"):
            tipos = obtener_tipos_usuario()
            tipos_map = {str(t.get("id_tipo_usuario")): t.get("nombre") for t in tipos} if tipos else {}
            tipo_options = list(tipos_map.keys()) if tipos_map else []

            if tipo_options:
                id_tipo_usuario = st.selectbox("Tipo de usuario", options=tipo_options, format_func=lambda k: f"{k} — {tipos_map[k]}")
                # convertir a int
                id_tipo_usuario = int(id_tipo_usuario)
            else:
                id_tipo_usuario = st.number_input("ID Tipo usuario (si no hay catálogo)", min_value=0, step=1)

            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
            dui = st.text_input("DUI / Identificación")
            direccion = st.text_input("Dirección")

            enviar = st.form_submit_button("Crear miembro")

            if enviar:
                payload = {
                    "id_tipo_usuario": id_tipo_usuario,
                    "nombre": nombre.strip() or None,
                    "apellido": apellido.strip() or None,
                    "dui": dui.strip() or None,
                    "direccion": direccion.strip() or None,
                }
                try:
                    newid = crear_miembro(payload)
                    if newid:
                        st.success(f"Miembro creado (ID {newid})")
                    else:
                        st.success("Miembro creado")
                except Exception as e:
                    st.error(f"Error al crear miembro: {e}")

    st.markdown("---")

    # --- Listado y acciones sobre miembros ---
    st.subheader("📋 Lista de miembros")
    try:
        miembros = obtener_miembros()
        if miembros:
            # mostrar tabla
            st.dataframe(miembros)

            # Seleccionar miembro para editar / eliminar
            ids = [m["id_miembro"] for m in miembros]
            sel = st.selectbox("Selecciona ID para editar / eliminar", options=[0] + ids, format_func=lambda x: "—" if x==0 else f"ID {x}")
            if sel and sel != 0:
                miembro = next((m for m in miembros if m["id_miembro"] == sel), None)
                if miembro:
                    st.markdown("### ✏️ Editar miembro")
                    with st.form("form_editar_miembro"):
                        tipos = obtener_tipos_usuario()
                        tipos_map = {str(t.get("id_tipo_usuario")): t.get("nombre") for t in tipos} if tipos else {}
                        tipo_default = str(miembro.get("id_tipo_usuario") or "")
                        if tipos_map:
                            id_tipo_usuario = st.selectbox("Tipo de usuario", options=list(tipos_map.keys()), index=(list(tipos_map.keys()).index(tipo_default) if tipo_default in tipos_map else 0), format_func=lambda k: f"{k} — {tipos_map[k]}")
                            id_tipo_usuario = int(id_tipo_usuario)
                        else:
                            id_tipo_usuario = st.number_input("ID Tipo usuario", value=int(miembro.get("id_tipo_usuario") or 0), min_value=0)

                        nombre = st.text_input("Nombre", value=miembro.get("nombre") or "")
                        apellido = st.text_input("Apellido", value=miembro.get("apellido") or "")
                        dui = st.text_input("DUI", value=miembro.get("dui") or "")
                        direccion = st.text_input("Dirección", value=miembro.get("direccion") or "")

                        guardar = st.form_submit_button("Guardar cambios")
                        eliminar = st.form_submit_button("Eliminar miembro")

                        if guardar:
                            payload = {
                                "id_tipo_usuario": id_tipo_usuario,
                                "nombre": nombre.strip() or None,
                                "apellido": apellido.strip() or None,
                                "dui": dui.strip() or None,
                                "direccion": direccion.strip() or None,
                            }
                            try:
                                ok = actualizar_miembro(sel, payload)
                                if ok:
                                    st.success("Miembro actualizado correctamente")
                                else:
                                    st.warning("No se actualizó (tal vez no hubo cambios).")
                            except Exception as e:
                                st.error(f"Error al actualizar: {e}")

                        if eliminar:
                            try:
                                ok = eliminar_miembro(sel)
                                if ok:
                                    st.success("Miembro eliminado")
                                else:
                                    st.warning("No se pudo eliminar el miembro.")
                            except Exception as e:
                                st.error(f"Error al eliminar: {e}")
        else:
            st.info("No hay miembros registrados aún.")
    except Exception as e:
        st.error(f"Error cargando miembros: {e}")



