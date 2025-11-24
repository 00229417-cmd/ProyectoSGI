# modulos/pages/reporte_page.py
import streamlit as st
from modulos.db import crud_reporte, crud_ciclo, crud_administrador

def render_reporte():
    st.title("Reportes")

    # Menú desplegable (mantener siempre como botón/desplegable como pediste)
    with st.expander("Generar nuevo reporte", expanded=True):
        # lista de tipos (puedes ampliar)
        tipos = ["mora", "cierre", "balance", "morosidad"]
        tipo = st.selectbox("Tipo de reporte", tipos)

        # Ciclos: cargar id y mostrar etiqueta; obligamos a seleccionar un id válido (int)
        ciclos = crud_ciclo.list_ciclos()  # se espera [(id, descripcion), ...] o lista de dicts
        ciclos_opts = []
        for c in ciclos:
            # soporta tu CRUD retornando dicts o tuplas
            if isinstance(c, dict):
                ciclos_opts.append((c.get("id_ciclo"), f"{c.get('id_ciclo')} - {c.get('fecha_inicio')}"))
            else:
                # tupla ejemplo (id, fecha_inicio)
                ciclos_opts.append((c[0], f"{c[0]}"))

        ciclos_map = {label: _id for _id, label in ciclos_opts}
        selected_label = st.selectbox("Ciclo (id)", [label for _id, label in ciclos_opts])
        id_ciclo = ciclos_map[selected_label]

        # Administrador (opcional) — cargar lista similar
        admins = crud_administrador.list_administradores()
        admin_map = {}
        admin_labels = []
        for a in admins:
            if isinstance(a, dict):
                lbl = f"{a.get('id_administrador')} - {a.get('nombre')}"
                admin_map[lbl] = a.get('id_administrador')
            else:
                lbl = f"{a[0]}"
                admin_map[lbl] = a[0]
            admin_labels.append(lbl)
        id_admin = admin_map[st.selectbox("Administrador (opcional)", ["-"] + admin_labels)] if admin_labels else None
        if id_admin == "-":
            id_admin = None

        desc = st.text_area("Descripción (opcional)")

        if st.button("Generar reporte"):
            # validar que id_ciclo sea entero
            try:
                id_ciclo_int = int(id_ciclo)
            except Exception:
                st.error("Selecciona un ciclo válido (ID numérico).")
                return

            ok, msg = crud_reporte.create_reporte(id_ciclo_int, id_admin, tipo, desc)
            if ok:
                st.success("Reporte creado y encola para generación.")
                st.rerun()
            else:
                st.error(f"Error creando reporte: {msg}")

    # listado de reportes
    st.markdown("---")
    st.header("Reportes generados")
    try:
        reportes = crud_reporte.list_reportes(limit=200)
        st.table(reportes)
    except Exception as e:
        st.error(f"Error listando reportes: {e}")


