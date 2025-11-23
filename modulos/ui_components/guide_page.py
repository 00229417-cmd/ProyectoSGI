# modulos/ui_components/guide_page.py
import streamlit as st
from modulos.ui_components.cards import (
    info_card,
    status_badge,
    stepper,
    progreso_bar,
    checklist_cierre,
    guided_tour,
)

def render_guide_page():
    st.title("Guía visual — ¿Qué hace cada sección?")

    st.markdown("### Resumen rápido")
    col1, col2, col3 = st.columns(3)
    with col1:
        info_card(
            "Registrar préstamo",
            "Registra la solicitud: monto, plazo y beneficiario. Ejemplo: $200 en 6 meses.",
            action_label="Ir a Préstamos",
            action_key="go_prestamos",
            emoji="💸",
        )
    with col2:
        info_card(
            "Registrar aporte",
            "Registra aportes por reunión; se actualiza caja y saldo de ahorro del miembro.",
            action_label="Ir a Aportes",
            action_key="go_aportes",
            emoji="🪙",
        )
    with col3:
        info_card(
            "Cerrar ciclo",
            "Consolida saldos, genera acta y calcula utilidades a repartir.",
            action_label="Iniciar cierre",
            action_key="go_cierre",
            emoji="📦",
        )

    st.markdown("---")
    st.header("Estados rápidos")
    st.write("Préstamo A:", status_badge("activo"))
    st.write("Préstamo B:", status_badge("vencido"))
    st.write("Préstamo C:", status_badge("mora"))

    st.markdown("---")
    st.header("Proceso: Otorgar préstamo")
    steps = [
        ("Solicitud", "Llenado de datos y documentos"),
        ("Evaluación", "Revisión por promotora/directiva"),
        ("Aprobación", "Decisión en reunión"),
        ("Desembolso", "Entregar fondos al miembro"),
    ]
    stepper(current_step=2, steps=steps)

    st.markdown("---")
    st.header("Progreso y checklist")
    progreso_bar(450, 1000, label="Pago acumulado")
    items = [
        {"key": "aportes", "label": "Todos los aportes registrados"},
        {"key": "actas", "label": "Actas firmadas"},
        {"key": "caja", "label": "Revisado saldo caja"},
    ]
    res = checklist_cierre(items)
    st.write(res)

    st.markdown("---")
    st.header("Guía interactiva")
    guided_tour(["Revisar miembros", "Registrar aporte", "Generar reporte de cierre", "Validar actas"])

    st.markdown("---")
    st.info("Consejo: mete esta página en el menú de ayuda para que usuarios nuevos la vean al ingresar.")
