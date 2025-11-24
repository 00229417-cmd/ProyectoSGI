# modulos/pages/reporte_page.py
import streamlit as st

# IMPORTS DIRECTOS (Opción A — recomendada)
from modulos.db.crud_reporte import create_reporte, list_reportes
from modulos.db.crud_ciclo import list_ciclos
from modulos.db.crud_administrador import list_administradores


def render_reporte():
    st.markdown("## 📄 Gestión de Reportes")

    # ================================
    # LISTAR REPORTES EXISTENTES
    # ================================
    st.markdown("### 📑 Historial de reportes generados")

    try:
        df = list_reportes()
        if df is not None and len(df) > 0:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No hay reportes generados.")
    except Exception as e:
        st.error(f"Error cargando reportes: {e}")

    st.divider()

    # ================================
    # BOTÓN DESPLEGABLE (OBLIGATORIO)
    # ================================
    with st.expander("➕ Crear nuevo reporte"):
        st.markdown("### 📝 Datos del nuevo reporte")

        # ----------------------------
        # Seleccionar ciclo
        # ----------------------------
        try:
            ciclos = list_ciclos()
            if ciclos is None or len(ciclos) == 0:
                st.warning("⚠ No hay ciclos registrados.")
                return
            
            ciclos_dict = {f"Ciclo {c['id_ciclo']} — {c['estado']}": c['id_ciclo'] for c in ciclos}
            ciclo_nombre = st.selectbox("Selecciona el ciclo:", list(ciclos_dict.keys()))
            id_ciclo = ciclos_dict[ciclo_nombre]

        except Exception as e:
            st.error(f"Error cargando ciclos: {e}")
            return

        # ----------------------------
        # Administrador que genera el reporte
        # ----------------------------
        try:
            admins = list_administradores()
            if admins is None or len(admins) == 0:
                st.warning("⚠ No hay administradores registrados.")
                return
            
            admins_dict = {f"{a['nombre']} {a['apellido']}": a['id_administrador'] for a in admins}
            admin_nombre = st.selectbox("Administrador que genera:", list(admins_dict.keys()))
            id_adm = admins_dict[admin_nombre]

        except Exception as e:
            st.error(f"Error cargando administradores: {e}")
            return

        # ----------------------------
        # Tipo de reporte
        # ----------------------------
        tipo = st.selectbox("Tipo de reporte:", ["mora", "balance", "cierre"])

        # ----------------------------
        # Descripción opcional
        # ----------------------------
        descripcion = st.text_area("Descripción (opcional):")

        # ----------------------------
        # GUARDAR REPORTE
        # ----------------------------
        if st.button("💾 Guardar reporte"):
            try:
                ok, msg = create_reporte(
                    id_ciclo=id_ciclo,
                    id_administrador=id_adm,
                    tipo=tipo,
                    descripcion=descripcion
                )

                if ok:
                    st.success("✅ Reporte creado correctamente")
                    st.rerun()
                else:
                    st.error(f"❌ No se pudo crear el reporte: {msg}")

            except Exception as e:
                st.error(f"Error creando reporte: {e}")

