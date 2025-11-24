# modulos/pages/miembros_page.py
import streamlit as st
import pandas as pd
from modulos.db.crud_miembros import list_members, create_member, update_member, delete_member

ICON_USER = "👤"
ICON_ADD = "➕"
ICON_EDIT = "✏️"
ICON_DELETE = "🗑️"
ICON_REFRESH = "🔄"

def render_miembros():
    st.header(f"{ICON_USER} Miembros")
    st.write("Administra los miembros: listar, crear, editar y eliminar. (No se modifica el esquema de la BD.)")

    # ---- Listar miembros ----
    st.subheader(f"{ICON_REFRESH} Lista de miembros")
    df, err = list_members(limit=1000)
    if err:
        st.error(err)
        # mostrar placeholder para que la página no se rompa
        st.info("Si las columnas esperadas no están presentes en la tabla 'miembro', revisa el esquema en phpMyAdmin.")
        st.stop()
    else:
        if df.empty:
            st.info("No hay miembros registrados aún.")
        else:
            # mostrar tabla interactiva
            st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # ---- Crear miembro ----
    st.subheader(f"{ICON_ADD} Crear nuevo miembro")
    with st.form("form_create_member", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre", placeholder="Juan")
            apellido = st.text_input("Apellido", placeholder="Pérez")
        with col2:
            dui = st.text_input("DUI (opcional)", placeholder="00000000-0")
            direccion = st.text_input("Dirección (opcional)")
        id_tipo = st.number_input("ID Tipo Usuario (opcional)", min_value=0, value=0, step=1)
        submit_create = st.form_submit_button("Crear miembro")
        if submit_create:
            # normalizar id_tipo: 0 -> None
            id_tipo_val = None if id_tipo == 0 else int(id_tipo)
            ok, res = create_member(
                nombre=nombre.strip() or None,
                apellido=apellido.strip() or None,
                dui=dui.strip() or None,
                direccion=direccion.strip() or None,
                id_tipo_usuario=id_tipo_val,
            )
            if ok:
                st.success("Miembro creado correctamente.")
                st.experimental_rerun()
            else:
                st.error(res)

    st.markdown("---")

    # ---- Editar / Eliminar miembro ----
    st.subheader(f"{ICON_EDIT} Editar / {ICON_DELETE} Eliminar miembro")
    if df is None or df.empty:
        st.info("No hay miembros para editar.")
        return

    # select member by id
    id_list = df["id_miembro"].tolist()
    selected_id = st.selectbox("Seleccionar miembro por ID", options=id_list, index=0)
    selected_row = df[df["id_miembro"] == selected_id].iloc[0]

    # show current values and allow edit
    with st.form("form_edit_member"):
        col1, col2 = st.columns(2)
        with col1:
            nombre_e = st.text_input("Nombre", value=str(selected_row.get("nombre", "") or ""))
            apellido_e = st.text_input("Apellido", value=str(selected_row.get("apellido", "") or ""))
        with col2:
            dui_e = st.text_input("DUI", value=str(selected_row.get("dui", "") or ""))
            direccion_e = st.text_input("Dirección", value=str(selected_row.get("direccion", "") or ""))
            id_tipo_e = st.number_input("ID Tipo Usuario", min_value=0, value=int(selected_row.get("id_tipo_usuario") or 0), step=1)
        btn_update = st.form_submit_button(f"{ICON_EDIT} Guardar cambios")
        btn_delete = st.form_submit_button(f"{ICON_DELETE} Eliminar miembro")

        if btn_update:
            id_tipo_val = None if id_tipo_e == 0 else int(id_tipo_e)
            ok, res = update_member(
                id_miembro=int(selected_id),
                nombre=nombre_e.strip() or None,
                apellido=apellido_e.strip() or None,
                dui=dui_e.strip() or None,
                direccion=direccion_e.strip() or None,
                id_tipo_usuario=id_tipo_val,
            )
            if ok:
                st.success("Miembro actualizado.")
                st.experimental_rerun()
            else:
                st.error(res)

        if btn_delete:
            confirm = st.checkbox("Confirmar eliminación (esto borrará el registro)", value=False)
            if confirm:
                ok, res = delete_member(int(selected_id))
                if ok:
                    st.success(f"Miembro eliminado ({res} fila(s) afectadas).")
                    st.experimental_rerun()
                else:
                    st.error(res)
            else:
                st.warning("Marca la casilla de confirmación para eliminar.")

    # fin render



