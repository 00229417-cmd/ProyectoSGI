# modulos/pages/grupo_page.py
import streamlit as st
from modulos.db import crud_grupo


# ======================================================
# RERUN SEGURO (reemplaza experimental_rerun)
# ======================================================
def safe_rerun():
    """
    Reintento seguro para forzar recarga sin usar experimental_rerun().
    """
    try:
        # API moderna
        if hasattr(st, "rerun"):
            st.rerun()
            return
    except Exception:
        pass

    # Fallback
    try:
        st.experimental_set_query_params(_reload="1")
    except Exception:
        pass


# ======================================================
# PÁGINA PRINCIPAL
# ======================================================
def render_grupo():
    st.header("🧩 Grupos")
    st.write("Administración de grupos: creación, consulta y eliminación.")

    # Toggle persistente
    if "show_crear_grupo" not in st.session_state:
        st.session_state["show_crear_grupo"] = False

    if st.button("Crear grupo 🔽"):
        st.session_state["show_crear_grupo"] = not st.session_state["show_crear_grupo"]

    # ======================================================
    # FORMULARIO DE CREACIÓN
    # ======================================================
    if st.session_state["show_crear_grupo"]:
        st.markdown("---")
        with st.form("form_grupo"):
            nombre = st.text_input("Nombre del grupo")
            id_ciclo = st.number_input("ID Ciclo", min_value=1, step=1)
            id_miembro = st.number_input("ID Miembro", min_value=1, step=1)
            id_promotora = st.number_input("ID Promotora", min_value=1, step=1)
            id_administrador = st.number_input("ID Administrador", min_value=1, step=1)
            tasa_interes = st.number_input("Tasa de interés (%)", min_value=0.0, step=0.1)
            tipo_multa = st.text_input("Tipo de multa")
            frecuencia = st.text_input("Frecuencia de reuniones")
            politicas = st.text_area("Políticas de préstamo")
            estado = st.text_input("Estado")

            submitted = st.form_submit_button("Guardar grupo ✅")

        if submitted:
            try:
                ok, msg = crud_grupo.create_grupo({
                    "id_ciclo": id_ciclo,
                    "id_miembro": id_miembro,
                    "id_promotora": id_promotora,
                    "id_administrador": id_administrador,
                    "nombre": nombre,
                    "tasa_interes": tasa_interes,
                    "tipo_de_multa": tipo_multa,
                    "frecuencia_reuniones": frecuencia,
                    "politicas_de_prestamo": politicas,
                    "estado": estado,
                })
            except TypeError:
                # fallback si tu función no recibe diccionarios
                ok, msg = crud_grupo.create_grupo(
                    id_ciclo, id_miembro, id_promotora, id_administrador,
                    nombre, tasa_interes, tipo_multa, frecuencia, politicas, estado
                )
            except Exception as e:
                ok, msg = False, str(e)

            if ok:
                st.success(msg or "Grupo creado exitosamente.")
                safe_rerun()
            else:
                st.error(f"Error guardando grupo: {msg}")

    # ======================================================
    # LISTADO DE GRUPOS
    # ======================================================
    st.markdown("---")
    st.subheader("📋 Grupos registrados")

    try:
        data = crud_grupo.list_grupos()

        if not data:
            st.info("No existen grupos registrados.")
            return

        for g in data:
            cols = st.columns([6, 2])
            with cols[0]:
                st.write(f"### {g.get('nombre','(sin nombre)')}")
                st.write(f"🆔 ID Grupo: {g.get('id_grupo')}")
                st.write(f"🔁 Ciclo: {g.get('id_ciclo')}")
                st.write(f"👤 Miembro: {g.get('id_miembro')}")
                st.write(f"📣 Promotora: {g.get('id_promotora')}")
                st.write(f"🧑‍💼 Administrador: {g.get('id_administrador')}")
                st.write(f"💱 Tasa Interés: {g.get('tasa_interes')}")
                st.write(f"⚖️ Multa: {g.get('tipo_de_multa')}")
                st.write(f"📅 Frecuencia: {g.get('frecuencia_reuniones')}")
                st.write(f"📘 Estado: {g.get('estado')}")

            with cols[1]:
                if st.button(f"Eliminar ❌ (ID {g.get('id_grupo')})", key=f"del_grupo_{g.get('id_grupo')}"):
                    try:
                        ok, msg = crud_grupo.delete_grupo(g.get("id_grupo"))
                        if ok:
                            st.success(msg or "Grupo eliminado.")
                            safe_rerun()
                        else:
                            st.error(msg)
                    except Exception as e:
                        st.error(f"Error eliminando grupo: {e}")

    except Exception as e:
        st.error(f"Error cargando grupos: {e}")

