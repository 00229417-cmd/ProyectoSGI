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
    Devuelve (obj, None) si se importa el módulo,
            (attr_obj, None) si se importa el atributo,
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
# UI
# ---------------------------
def render_reporte():
    st.markdown("# 📄 Reportes")
    st.write("Genera reportes (mora, cierre, balance).")

    # Conexión con usuario en sesión
    usuario_sesion = st.session_state.get("usuario") or ""
    st.caption(f"Usuario en sesión: {usuario_sesion or '—'}")

    # Obtener ciclos (si la función existe)
    ciclos_options = []
    ciclo_selected = None
    if list_ciclos:
        try:
            ciclos = list_ciclos(limit=500) if callable(list_ciclos) else []
            # ciclos puede ser lista de dicts o lista de tuplas; estandarizamos
            for c in ciclos:
                if isinstance(c, dict):
                    ciclos_options.append((int(c.get("id_ciclo")), str(c.get("fecha_inicio") or c.get("nombre") or c.get("id_ciclo"))))
                elif isinstance(c, (list, tuple)) and len(c) >= 1:
                    # asumimos (id, ...) o (id, desc)
                    try:
                        cid = int(c[0])
                    except Exception:
                        cid = None
                    label = c[1] if len(c) > 1 else str(cid)
                    ciclos_options.append((cid, str(label)))
        except Exception as e:
            st.error(f"Error obteniendo ciclos: {e}")

    # Convertir opciones para streamlit
    ciclo_map = {str(cid): cid for cid, _ in ciclos_options if cid is not None}
    ciclo_labels = [f"{cid} — {lbl}" for cid, lbl in ciclos_options]

    # Formulario
    with st.form("form_reporte"):
        col1, col2 = st.columns([2, 1])
        with col1:
            tipo = st.selectbox("Tipo de reporte", ["mora", "cierre", "balance", "morosidad"], index=0)
            descripcion = st.text_area("Descripción (opcional)", height=120)
        with col2:
            # si tenemos ciclos, mostrar select, sino entrada libre (validada)
            if ciclo_labels:
                sel = st.selectbox("Ciclo (opcional)", ["Ninguno"] + ciclo_labels)
                if sel != "Ninguno":
                    # extraer id antes del ' — '
                    cid_str = sel.split("—", 1)[0].strip()
                    try:
                        ciclo_selected = int(cid_str)
                    except Exception:
                        ciclo_selected = None
            else:
                # permitir ingresar id de ciclo si se conoce
                raw = st.text_input("ID Ciclo (opcional, numérico)")
                try:
                    ciclo_selected = int(raw) if raw.strip() != "" else None
                except Exception:
                    ciclo_selected = None

            admin_manual = st.text_input("Usuario / administrador (opcional)", value=usuario_sesion)
            submit = st.form_submit_button("Crear reporte")

        if submit:
            # Validaciones simples
            id_ciclo_to_send: Optional[int] = None
            if ciclo_selected is not None:
                try:
                    id_ciclo_to_send = int(ciclo_selected)
                except Exception:
                    st.warning("El ID de ciclo no es un entero válido. Se enviará NULL al crear el reporte.")
                    id_ciclo_to_send = None

            # Intentar llamar a create_reporte de forma segura, detectando firma
            if create_reporte is None:
                st.error("La función create_reporte no está disponible. Verifica modulos/db/crud_reporte.py")
            else:
                try:
                    sig = inspect.signature(create_reporte)
                    params = sig.parameters
                    # Construir argumentos según lo que acepte la función
                    call_kwargs = {}
                    # posibles nombres que la función podría pedir:
                    # ('id_ciclo','id_administrador','tipo','descripcion','estado','usuario', 'desc')
                    if "id_ciclo" in params:
                        call_kwargs["id_ciclo"] = id_ciclo_to_send
                    elif "ciclo_id" in params:
                        call_kwargs["ciclo_id"] = id_ciclo_to_send

                    # administrador / usuario
                    if "id_administrador" in params:
                        # si viene texto en admin_manual, tratamos de convertir a int si aplica
                        try:
                            call_kwargs["id_administrador"] = int(admin_manual) if str(admin_manual).isdigit() else admin_manual
                        except Exception:
                            call_kwargs["id_administrador"] = admin_manual
                    elif "usuario" in params:
                        call_kwargs["usuario"] = admin_manual
                    elif "id_adm" in params:
                        call_kwargs["id_adm"] = admin_manual

                    # tipo / tipo_reporte
                    if "tipo" in params:
                        call_kwargs["tipo"] = tipo
                    elif "tipo_reporte" in params:
                        call_kwargs["tipo_reporte"] = tipo

                    # descripcion / desc
                    if "descripcion" in params:
                        call_kwargs["descripcion"] = descripcion or None
                    elif "desc" in params:
                        call_kwargs["desc"] = descripcion or None

                    # Si la función solo recibe 1 posicional (por ejemplo un dict), intentar pasar un dict
                    if len(params) == 1 and next(iter(params.values())).kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
                        # crear payload mínimamente útil
                        payload = {
                            "id_ciclo": id_ciclo_to_send,
                            "id_administrador": admin_manual,
                            "tipo": tipo,
                            "descripcion": descripcion or None
                        }
                        result = create_reporte(payload)  # intento posicional
                    else:
                        # intentar llamada con kwargs
                        result = create_reporte(**call_kwargs)

                    st.success(f"Reporte solicitado. Resultado: {result}")
                except TypeError as te:
                    st.error(f"Error al llamar create_reporte (firma inesperada): {te}")
                except Exception as e:
                    st.error(f"Error creando reporte: {e}")


    # Mostrar lista de reportes existentes (si hay list_reportes)
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

        # Estándar simple: si rows es lista de dicts mostramos dataframe
        if isinstance(rows, list) and isinstance(rows[0], dict):
            st.table(rows)
        else:
            # intentar convertir cada fila a dict si viene como tupla
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


# Exponer la función principal con un nombre común que app.py puede invocar
def render_reporte_page():
    render_reporte()


# compatibilidad con nombres alternativos que app.py pueda intentar
def render_reporte():
    render_reporte()


if __name__ == "__main__":
    render_reporte()


