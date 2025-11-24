# modulos/pages/reporte_page.py
import importlib
import inspect
from typing import Optional

import streamlit as st

st.set_page_config(layout="wide")

# ---------------------------
# Helpers para imports robustos
# ---------------------------
def safe_import(module_path: str, attr: str = None):
    """
    Intenta importar un módulo o un atributo dentro del módulo.
    Devuelve (obj, None) si se importa correctamente,
            (None, error_str) si hay error.
    """
    try:
        module = importlib.import_module(module_path)
        if attr:
            return getattr(module, attr), None
        return module, None
    except Exception as e:
        return None, str(e)


# Intentar importar funciones CRUD concretas (si existen)
create_reporte, err_cr = safe_import("modulos.db.crud_reporte", "create_reporte")
list_reportes, err_lr = safe_import("modulos.db.crud_reporte", "list_reportes")
list_ciclos, err_lc = safe_import("modulos.db.crud_ciclo", "list_ciclos")
list_administradores, err_la = safe_import("modulos.db.crud_administrador", "list_administradores")

# ---------------------------
# UI principal (única definición)
# ---------------------------
def render_reporte():
    st.markdown("# 📄 Reportes")
    st.write("Genera reportes (mora, cierre, balance).")

    usuario_sesion = st.session_state.get("usuario") or ""
    st.caption(f"Usuario en sesión: {usuario_sesion or '—'}")

    # Preparar opciones de ciclos si la función existe
    ciclos_options = []
    ciclo_selected = None
    if list_ciclos:
        try:
            ciclos = list_ciclos(limit=500) if callable(list_ciclos) else []
            for c in ciclos:
                if isinstance(c, dict):
                    cid = c.get("id_ciclo") or c.get("id") or None
                    label = c.get("fecha_inicio") or c.get("nombre") or str(cid)
                    try:
                        cid = int(cid) if cid is not None else None
                    except Exception:
                        cid = None
                    ciclos_options.append((cid, str(label)))
                elif isinstance(c, (list, tuple)) and len(c) >= 1:
                    try:
                        cid = int(c[0])
                    except Exception:
                        cid = None
                    label = c[1] if len(c) > 1 else str(cid)
                    ciclos_options.append((cid, str(label)))
        except Exception as e:
            st.error(f"Error obteniendo ciclos: {e}")

    # Construir UI del formulario
    with st.form("form_reporte"):
        left, right = st.columns([2, 1])
        with left:
            tipo = st.selectbox("Tipo de reporte", ["mora", "cierre", "balance", "morosidad"])
            descripcion = st.text_area("Descripción (opcional)", height=120)
        with right:
            # Selección de ciclo (si hay)
            if ciclos_options:
                labels = [f"{cid} — {lbl}" for cid, lbl in ciclos_options]
                sel = st.selectbox("Ciclo (opcional)", ["Ninguno"] + labels)
                if sel != "Ninguno":
                    cid_str = sel.split("—", 1)[0].strip()
                    try:
                        ciclo_selected = int(cid_str)
                    except Exception:
                        ciclo_selected = None
            else:
                raw = st.text_input("ID Ciclo (opcional, numérico)")
                try:
                    ciclo_selected = int(raw) if raw.strip() != "" else None
                except Exception:
                    ciclo_selected = None

            admin_manual = st.text_input("Usuario / administrador (opcional)", value=usuario_sesion)
            submit = st.form_submit_button("Crear reporte")

        if submit:
            id_ciclo_to_send: Optional[int] = None
            if ciclo_selected is not None:
                try:
                    id_ciclo_to_send = int(ciclo_selected)
                except Exception:
                    id_ciclo_to_send = None
                    st.warning("ID de ciclo inválido; se enviará NULL si create_reporte lo acepta.")

            if create_reporte is None:
                st.error("La función create_reporte no está disponible. Verifica modulos/db/crud_reporte.py")
            else:
                try:
                    sig = inspect.signature(create_reporte)
                    params = sig.parameters
                    call_kwargs = {}

                    if "id_ciclo" in params:
                        call_kwargs["id_ciclo"] = id_ciclo_to_send
                    elif "ciclo_id" in params:
                        call_kwargs["ciclo_id"] = id_ciclo_to_send

                    if "id_administrador" in params:
                        try:
                            call_kwargs["id_administrador"] = int(admin_manual) if str(admin_manual).isdigit() else admin_manual
                        except Exception:
                            call_kwargs["id_administrador"] = admin_manual
                    elif "usuario" in params:
                        call_kwargs["usuario"] = admin_manual
                    elif "id_adm" in params:
                        call_kwargs["id_adm"] = admin_manual

                    if "tipo" in params:
                        call_kwargs["tipo"] = tipo
                    elif "tipo_reporte" in params:
                        call_kwargs["tipo_reporte"] = tipo

                    if "descripcion" in params:
                        call_kwargs["descripcion"] = descripcion or None
                    elif "desc" in params:
                        call_kwargs["desc"] = descripcion or None

                    # Si la función solo espera 1 argumento posicional, le pasamos un dict
                    only_one_param = (len(params) == 1 and next(iter(params.values())).kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD))
                    if only_one_param:
                        payload = {
                            "id_ciclo": id_ciclo_to_send,
                            "id_administrador": admin_manual,
                            "tipo": tipo,
                            "descripcion": descripcion or None
                        }
                        result = create_reporte(payload)
                    else:
                        result = create_reporte(**call_kwargs)

                    st.success(f"Reporte solicitado. Resultado: {result}")
                except TypeError as te:
                    st.error(f"Error al llamar create_reporte (firma inesperada): {te}")
                except Exception as e:
                    st.error(f"Error creando reporte: {e}")

    # Mostrar reportes existentes si la función existe
    st.markdown("---")
    st.subheader("Reportes recientes")
    if list_reportes is None:
        st.info("Función list_reportes no disponible. Si existe, crea modulos/db/crud_reporte.list_reportes")
        return

    try:
        rows = list_reportes(limit=200) if callable(list_reportes) else []
        if not rows:
            st.write("No hay reportes para mostrar.")
            return

        if isinstance(rows, list) and isinstance(rows[0], dict):
            st.table(rows)
        else:
            processed = []
            for r in rows:
                if isinstance(r, dict):
                    processed.append(r)
                elif isinstance(r, (list, tuple)):
                    processed.append({"fila": r})
                else:
                    processed.append({"value": r})
            st.table(processed)
    except Exception as e:
        st.error(f"Error cargando lista de reportes: {e}")


# Alias seguro que app.py puede importar (un único punto de entrada)
def render_reporte_page():
    return render_reporte()


# También exponer el nombre simple que tu app podría buscar
def render_reporte():
    return render_reporte_page()


if __name__ == "__main__":
    render_reporte_page()

