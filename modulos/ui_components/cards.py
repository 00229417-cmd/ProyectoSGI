# modulos/ui_components/cards.py
import streamlit as st

# -------------------------
# Info card (visual help)
# -------------------------
def info_card(title: str, body: str, action_label: str = None, action_key: str = None, emoji: str = "📌"):
    """
    Muestra una tarjeta explicativa con título, texto y un botón opcional.
    """
    with st.container():
        st.markdown(
            f"""
            <div style="border:1px solid #e6e6e6;padding:14px;border-radius:10px;background:#fff;">
              <div style="font-size:18px;font-weight:600">{emoji} {title}</div>
              <div style="color:#555;margin-top:8px">{body}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if action_label:
            if st.button(action_label, key=action_key):
                return True
    return False


# -------------------------
# Status badge (emoji)
# -------------------------
def status_badge(status: str) -> str:
    if status is None:
        return "ℹ️ Desconocido"
    s = status.lower()
    if s in ("activo", "activo/a", "ok", "operativo"):
        return "✅ Activo"
    if s in ("vencido", "vencida", "vencimiento"):
        return "⚠️ Vencido"
    if s in ("mora", "moroso", "en mora"):
        return "❌ En mora"
    if s in ("pendiente", "por revisar"):
        return "🟠 Pendiente"
    return "ℹ️ " + status


# -------------------------
# Stepper (proceso en pasos)
# -------------------------
def stepper(current_step: int, steps: list):
    """
    steps: list of tuples (title, short_description)
    current_step: 1-based index
    """
    cols = st.columns(len(steps))
    for i, (title, desc) in enumerate(steps, start=1):
        with cols[i - 1]:
            if i < current_step:
                st.markdown(f"**✅ {i}. {title}**")
                st.caption(desc)
            elif i == current_step:
                st.markdown(f"**🔵 {i}. {title}**")
                st.caption(desc)
            else:
                st.markdown(f"**{i}. {title}**")
                st.caption(desc)


# -------------------------
# Progress helper
# -------------------------
def progreso_bar(valor_actual: float, total: float, label: str = "Progreso"):
    porcentaje = int((valor_actual / total) * 100) if total else 0
    st.metric(label, f"{porcentaje}%")
    st.progress(porcentaje)


# -------------------------
# Empty state helper
# -------------------------
def empty_state(title: str, text: str, cta_label: str = None, cta_key: str = None):
    st.info(f"**{title}**\n\n{text}")
    if cta_label and st.button(cta_label, key=cta_key):
        return True
    return False


# -------------------------
# Checklist (for validations)
# -------------------------
def checklist_cierre(items: list):
    """
    items: list of dicts {"key": "id", "label": "texto"}
    returns dict key->bool
    """
    st.header("Checklist requerida")
    results = {}
    for it in items:
        key = it.get("key") or it.get("label")
        results[key] = st.checkbox(it.get("label"), key=f"chk_{key}")
    return results


# -------------------------
# Simple guided tour (stateful)
# -------------------------
def guided_tour(step_titles: list):
    if "tour_step" not in st.session_state:
        st.session_state.tour_step = 0

    if st.button("Iniciar tour"):
        st.session_state.tour_step = 1

    if st.session_state.tour_step > 0:
        i = st.session_state.tour_step
        st.info(f"**Paso {i}/{len(step_titles)}** — {step_titles[i-1]}")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Anterior"):
                st.session_state.tour_step = max(1, st.session_state.tour_step - 1)
        with col2:
            if st.button("Siguiente"):
                st.session_state.tour_step = min(len(step_titles), st.session_state.tour_step + 1)
        if st.button("Finalizar tour"):
            st.session_state.tour_step = 0
            st.success("Tour finalizado. Puedes repetirlo cuando quieras.")


# -------------------------
# Small helpers for microcopy
# -------------------------
def help_text(text: str):
    st.caption(text)
