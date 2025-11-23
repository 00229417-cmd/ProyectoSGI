# modulos/pages/miembros_page.py

import streamlit as st
from modulos.db.crud_miembros import (
    list_members,
    search_members,
    create_member,
    update_member,
    delete_member,
)

# -----------------------------
# --- ESTILOS PREMIUM ----------
# -----------------------------
st.markdown(
    """
    <style>
    .member-card {
        background: rgba(255,255,255,0.03);
        padding: 18px;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.05);
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
        margin-bottom: 18px;
    }
    .table-container {
        background: rgba(255,255,255,0.03);
        padding: 12px;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.05);
        box-shadow: 0 6px 18px rgba(0,0,0,0.28);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ================================
# PAGE TITLE
# ================================
st.header("👥 Gestión de Miembros")

st.write("Administra los miembros del sistema GAPC.")

# ================================
# BUSCADOR
# ================================
st.subheader("🔎 Buscar miembros")

search = st.text_input("Buscar por nombre, apellido o DUI:")

if search.strip():
    members = search_members(search)
else:
    members = list_members()

# ================================
# TABLA DE RESULTADOS
# ================================
st.subheader("📋 Lista de miembros")

if members:
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.dataframe(members, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No se encontraron miembros.")

# =======================================================
# FORMULARIO DE CREACIÓN
# =======================================================
st.subheader("➕ Registrar nuevo miembro")

with st.form("create_member_form"):
    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        dui = st.text_input("DUI (opcional)")
    with col2:
        id_tipo_usuario = st.number_input("ID Tipo de usuario", min_value=1, step=1)
        direccion = st.text_area("Dirección (opcional)")

    submit_create = st.form_submit_button("Crear miembro")

    if submit_create:
        if not nombre or not apellido:
            st.error("Nombre y apellido son obligatorios.")
        else:
            ok = create_member(
                id_tipo_usuario=id_tipo_usuario,
                nombre=nombre,
                apellido=apellido,
                dui=dui,
                direccion=direccion,
            )
            if ok:
                st.success("Miembro creado correctamente.")
                st.experimental_rerun()
            else:
                st.error("Error creando el miembro.")

# =======================================================
# SECCIÓN DE EDICIÓN / ELIMINACIÓN
# =======================================================
st.subheader("✏️ Editar o eliminar miembro")

if not members:
    st.info("No hay miembros para editar.")
else:
    ids = [m["id_miembro"] for m in members]
    selected_id = st.selectbox("Seleccionar miembro por ID:", ids)

    m = next((x for x in members if x["id_miembro"] == selected_id), None)

    if m:
        with st.expander(f"Editar miembro: {m['nombre']} {m['apellido']}", expanded=False):

            with st.form("edit_member_form"):
                col1, col2 = st.columns(2)

                with col1:
                    new_nombre = st.text_input("Nombre", m["nombre"])
                    new_apellido = st.text_input("Apellido", m["apellido"])
                    new_dui = st.text_input("DUI", m["dui"])
                with col2:
                    new_tipo = st.number_input("ID Tipo usuario", min_value=1, value=m["id_tipo_usuario"])
                    new_direccion = st.text_area("Dirección", m["direccion"] or "")

                col3, col4 = st.columns(2)
                submit_edit = col3.form_submit_button("Guardar cambios")
                delete_btn = col4.form_submit_button("Eliminar miembro")

                if submit_edit:
                    ok = update_member(
                        member_id=selected_id,
                        id_tipo_usuario=new_tipo,
                        nombre=new_nombre,
                        apellido=new_apellido,
                        dui=new_dui,
                        direccion=new_direccion,
                    )
                    if ok:
                        st.success("Miembro actualizado correctamente.")
                        st.experimental_rerun()
                    else:
                        st.error("Error al actualizar miembro.")

                if delete_btn:
                    ok = delete_member(selected_id)
                    if ok:
                        st.warning("Miembro eliminado.")
                        st.experimental_rerun()
                    else:
                        st.error("No se pudo eliminar el miembro.")

