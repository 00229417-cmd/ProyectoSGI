# modulos/pages/promotora_page.py
import streamlit as st
from modulos.db import crud_promotora

def safe_rerun():
    """
    Reintento seguro para forzar un rerun de Streamlit.
    Intenta st.rerun() (API moderna). Si no existe, hace un fallback
    modificando parámetros de query para forzar recarga en entornos limitados.
    """
    try:
        # API moderna
        if hasattr(st, "rerun") and callable(st.rerun):
            st.rerun()
            return
    except Exception:
        pass

    # Fallback: cambiar query params para forzar efecto similar a rerun
    try:
        st.experimental_set_query_params(_reload="1")
    except Exception:
        # Si tampoco funciona, no hacemos nada — al menos evitamos crash.
        return

def render_promotora():
    st.header("📣 Promotoras")
    st.write("Administración de promotoras — crear, listar y eliminar")

    # toggle persistente
    if "show_crear_promotora" not in st.session_state:
        st.session_state["show_crear_promotora"] = False

    if st.button("Crear promotora 🔽"):
        st.session_state["show_crear_promotora"] = not st.session_state["show_crear_promotora"]

    # Formulario dentro de toggle
    if st.session_state["show_crear_promotora"]:
        st.markdown("---")
        with st.form("form_promotora"):
            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
            telefono = st.text_input("Teléfono")
            correo = st.text_input("Correo")
            distrito = st.text_input("Distrito")
            submitted = st.form_submit_button("Guardar promotora ✅")

        if submitted:
            try:
                ok, msg = crud_promotora.create_promotora({
                    "nombre": nombre,
                    "apellido": apellido,
                    "telefono": telefono,
                    "correo": correo,
                    "distrito": distrito,
                })
            except TypeError:
                # Si tu create_promotora no espera dict sino args, intenta llamar de otra forma
                try:
                    ok, msg = crud_promotora.create_promotora(nombre, apellido, telefono, correo, distrito)
                except Exception as e:
                    st.error(f"Error al crear promotora (llamada fallback): {e}")
                    ok, msg = False, str(e)
            except Exception as e:
                ok, msg = False, str(e)

            if ok:
                st.success(msg or "Promotora creada.")
                # forzar refresco para ver la nueva fila — uso safe_rerun
                safe_rerun()
            else:
                st.error(f"Error guardando promotora: {msg}")

    st.markdown("---")
    st.subheader("Promotoras registradas")
    try:
        rows = crud_promotora.list_promotoras()
        if not rows:
            st.info("No hay promotoras registradas.")
        else:
            # mostrar tabla con botón eliminar por fila
            # asumimos que rows es lista de dicts; si es otra estructura, ajusta
            for r in rows:
                cols = st.columns([6, 3])
                with cols[0]:
                    st.write(f"**{r.get('nombre','')} {r.get('apellido','')}** — {r.get('distrito','')}")
                    st.write(f"📧 {r.get('correo','')} — 📞 {r.get('telefono','')}")
                with cols[1]:
                    if st.button(f"Eliminar ❌ ({r.get('id_promotora')})", key=f"del_prom_{r.get('id_promotora')}"):
                        try:
                            ok, msg = crud_promotora.delete_promotora(r.get('id_promotora'))
                            if ok:
                                st.success(msg or "Eliminado.")
                                safe_rerun()
                            else:
                                st.error(msg or "No se pudo eliminar.")
                        except Exception as e:
                            st.error(f"Error al eliminar: {e}")

    except Exception as e:
        st.error(f"Error cargando promotoras: {e}")

