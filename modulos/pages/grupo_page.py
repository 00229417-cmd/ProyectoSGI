# modulos/pages/grupo_page.py
import streamlit as st
from modulos.db import crud_grupo

# ======================================================
# RERUN SEGURO (reemplaza experimental_rerun)
# ======================================================
def safe_rerun():
    """
    Forzar recarga de la app sin usar st.experimental_rerun (no disponible).
    Intenta st.rerun() y si no existe usa un pequeño 'trigger' por query params.
    """
    try:
        if hasattr(st, "rerun"):
            st.rerun()
            return
    except Exception:
        pass

    try:
        # fallback: cambia query param para forzar recarga en muchas versiones
        st.experimental_set_query_params(_reload="1")
    except Exception:
        # último recurso: nada más que mostrar aviso
        st.info("Por favor recarga la página manualmente (F5).")


# ======================================================
# PÁGINA PRINCIPAL
# ======================================================
def render_grupo():
    st.header("🧩 Grupos")
    st.write("Administración de grupos: creación, consulta y eliminación.")

    # Toggle persistente
    if "show_crear_grupo" not in st.session_state:
        st.session_state["show_crear_grupo"] = False

    # botón desplegable (toggle)
    if st.button("Crear grupo 🔽"):
        st.session_state["show_crear_grupo"] = not st.session_state["show_crear_grupo"]

    # ======================================================
    # FORMULARIO DE CREACIÓN
    # ======================================================
    if st.session_state["show_crear_grupo"]:
        st.markdown("---")
        with st.form("form_grupo"):
            nombre = st.text_input("Nombre del grupo")
            id_ciclo = st.number_input("ID Ciclo", min_value=0, step=1, value=0)
            id_miembro = st.number_input("ID Miembro", min_value=0, step=1, value=0)
            id_promotora = st.number_input("ID Promotora", min_value=0, step=1, value=0)
            id_administrador = st.number_input("ID Administrador", min_value=0, step=1, value=0)
            tasa_interes = st.number_input("Tasa de interés (%)", min_value=0.0, step=0.1, value=0.0)
            tipo_multa = st.text_input("Tipo de multa")
            frecuencia = st.text_input("Frecuencia de reuniones")
            politicas = st.text_area("Políticas de préstamo")
            estado = st.text_input("Estado")
            submitted = st.form_submit_button("Guardar grupo ✅")

        if submitted:
            # intenta usar API que tengas en crud_grupo
            try:
                # 1) si tu create_grupo acepta un dict
                ok, msg = crud_grupo.create_grupo({
                    "id_ciclo": id_ciclo or None,
                    "id_miembro": id_miembro or None,
                    "id_promotora": id_promotora or None,
                    "id_administrador": id_administrador or None,
                    "nombre": nombre,
                    "tasa_interes": tasa_interes,
                    "tipo_de_multa": tipo_multa,
                    "frecuencia_reuniones": frecuencia,
                    "politicas_de_prestamo": politicas,
                    "estado": estado,
                })
            except TypeError:
                # 2) fallback: si tu función recibe args posicionales
                try:
                    ok, msg = crud_grupo.create_grupo(
                        id_ciclo, id_miembro, id_promotora, id_administrador,
                        nombre, tasa_interes, tipo_multa, frecuencia, politicas, estado
                    )
                except Exception as e:
                    ok, msg = False, str(e)
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
        grupos = crud_grupo.list_grupos()
    except Exception as e:
        st.error(f"Error cargando grupos: {e}")
        return

    if not grupos:
        st.info("No existen grupos registrados.")
        return

    # Mostrar cada grupo en tarjeta simple con botón eliminar
    for g in grupos:
        idg = g.get("id_grupo") or g.get("id") or "(sin id)"
        cols = st.columns([6, 2])
        with cols[0]:
            st.write(f"### {g.get('nombre','(sin nombre)')}")
            st.write(f"🆔 ID Grupo: {idg}")
            if "id_ciclo" in g: st.write(f"🔁 Ciclo: {g.get('id_ciclo')}")
            if "id_miembro" in g: st.write(f"👤 Miembro: {g.get('id_miembro')}")
            if "id_promotora" in g: st.write(f"📣 Promotora: {g.get('id_promotora')}")
            if "id_administrador" in g: st.write(f"🧑‍💼 Admin: {g.get('id_administrador')}")
            if "tasa_interes" in g: st.write(f"💱 Tasa Interés: {g.get('tasa_interes')}")
            if "tipo_de_multa" in g: st.write(f"⚖️ Multa: {g.get('tipo_de_multa')}")
            if "frecuencia_reuniones" in g: st.write(f"📅 Frecuencia: {g.get('frecuencia_reuniones')}")
            if "estado" in g: st.write(f"📘 Estado: {g.get('estado')}")

        with cols[1]:
            if st.button(f"Eliminar ❌ (ID {idg})", key=f"del_grupo_{idg}"):
                try:
                    ok, msg = crud_grupo.delete_grupo(idg)
                except TypeError:
                    # fallback si delete_grupo espera int
                    ok, msg = crud_grupo.delete_grupo(int(idg))
                except Exception as e:
                    ok, msg = False, str(e)

                if ok:
                    st.success(msg or "Grupo eliminado.")
                    safe_rerun()
                else:
                    st.error(msg or "Error al eliminar.")



