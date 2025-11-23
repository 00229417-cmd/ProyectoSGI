# fragmento a usar en app.py -> dentro del with st.sidebar: ... reemplazar la porción correspondiente
with st.sidebar:
    st.header("Menú 📋")
    opcion = st.selectbox("Selecciona una opción", ["Dashboard", "Miembros", "Aportes", "Préstamos", "Caja", "Reportes"])

    st.divider()
    st.caption(f"Conectado: {st.session_state.get('usuario') or 'Invitado'}")

    # Mostrar registro admin SOLO si el usuario tiene role 'admin'
    user_role = None
    # si tienes role guardado en session_state, úsalo; aquí tratamos de leerlo
    try:
        user_role = st.session_state.get("user_role") or st.session_state.get("role")
    except Exception:
        user_role = None

    if user_role == "admin":
        st.markdown("### Registro (admin)")
        with st.expander("Crear usuario / miembro"):
            from modulos.db.crud_users import create_user_and_member
            ru = st.text_input("Usuario (nuevo) - admin", key="side_ru")
            rn = st.text_input("Nombre completo - admin", key="side_rn")
            rd = st.text_input("Identificación (opcional)", key="side_rd")
            rt = st.text_input("Teléfono (opcional)", key="side_rt")
            rdir = st.text_input("Dirección (opcional)", key="side_rdir")
            rpw = st.text_input("Contraseña", type="password", key="side_rpw")
            rpw2 = st.text_input("Confirmar contraseña", type="password", key="side_rpw2")
            if st.button("Crear usuario (admin)", use_container_width=True):
                if not ru or not rpw:
                    st.error("Usuario y contraseña requeridos.")
                elif rpw != rpw2:
                    st.error("Contraseñas no coinciden.")
                else:
                    user_id = create_user_and_member(
                        username=ru,
                        password=rpw,
                        full_name=rn,
                        dni=rd,
                        telefono=rt,
                        direccion=rdir,
                        role="user"
                    )
                    if user_id:
                        st.success("Usuario y miembro creados correctamente.")
                    else:
                        st.error("Error al crear usuario/miembro.")
    # Botón cerra sesión
    if st.button("Cerrar sesión 🔒", use_container_width=True):
        st.session_state["session_iniciada"] = False
        st.session_state["usuario"] = None
        st.session_state["usuario_id"] = None
        # si guardaste role en session_state, limpiar
        if "user_role" in st.session_state:
            del st.session_state["user_role"]
        st.rerun()




