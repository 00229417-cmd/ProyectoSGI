# modulos/pages/miembros_page.py
import streamlit as st
from modulos.db.crud_miembros import list_miembros, create_miembro, get_miembro_by_id, update_miembro, delete_miembro

def render_miembros():
    st.header("Miembros")
    st.subheader("Lista de miembros registrados")

    # botón nuevo arriba
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("➕ Nuevo miembro"):
            st.session_state["_show_new_miembro"] = True

    # tabla de miembros
    miembros = list_miembros(limit=500)
    if not miembros:
        st.info("No hay miembros registrados todavía.")
    else:
        # mostramos tabla (Streamlit Dataframe)
        st.dataframe(miembros)

    st.markdown("---")

    # formulario: crear / editar
    if st.session_state.get("_show_new_miembro", False):
        st.markdown("### Crear nuevo miembro")
        with st.form("create_miembro_form", clear_on_submit=True):
            nombre = st.text_input("Nombre", "")
            apellido = st.text_input("Apellido", "")
            dui = st.text_input("DUI", "")
            direccion = st.text_input("Dirección", "")
            submitted = st.form_submit_button("Guardar")
            if submitted:
                ok = create_miembro(nombre=nombre, apellido=apellido, dui=dui, direccion=direccion)
                if ok:
                    st.success("Miembro creado correctamente ✅")
                    st.session_state["_show_new_miembro"] = False
                    st.experimental_rerun()
                else:
                    st.error("No se pudo crear miembro.")

    # Quick edit (selección por id)
    st.markdown("#### Editar / Eliminar miembro (rápido)")
    id_sel = st.number_input("ID miembro", min_value=0, step=1, value=0)
    if id_sel:
        m = get_miembro_by_id(int(id_sel))
        if not m:
            st.warning("Miembro no encontrado.")
        else:
            with st.form("edit_miembro_form"):
                nombre = st.text_input("Nombre", value=m.get("nombre", ""))
                apellido = st.text_input("Apellido", value=m.get("apellido", ""))
                dui = st.text_input("DUI", value=m.get("dui",""))
                direccion = st.text_input("Dirección", value=m.get("direccion",""))
                btn_upd = st.form_submit_button("Actualizar")
                btn_del = st.form_submit_button("Eliminar")
                if btn_upd:
                    update_miembro(id_miembro=id_sel, nombre=nombre, apellido=apellido, dui=dui, direccion=direccion)
                    st.success("Miembro actualizado.")
                    st.experimental_rerun()
                if btn_del:
                    delete_miembro(id_miembro=id_sel)
                    st.success("Miembro eliminado.")
                    st.experimental_rerun()

