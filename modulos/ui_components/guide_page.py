# modulos/ui_components/guide_page.py
import streamlit as st
from modulos.ui_components.cards import (
    info_card,
    status_badge,
    stepper,
    progreso_bar,
    empty_state,
    checklist_cierre,
    guided_tour,
    help_text,
)

def render_guide_page():
    st.title("Guía visual — ¿Qué hace cada sección?")

    st.markdown("### Resumen rápido")
    col1, col2, col3 = st.columns(3)
    with col1:
        info_card(
            "Registrar préstamo",
            "Este módulo permite registrar solicitudes, validar documentos y generar cuotas automáticamente. Ejemplo: $200 en 6 meses.",
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
            "Proceso que consolida saldos, genera acta y calcula utilidades a repartir.",
            action_label="Iniciar cierre",
            action_key="go_cierre",
            emoji="📦",
        )

    st.markdown("---")
    st.header("Indicadores y estados rápidos")
    st.write("Los badges ayudan a entender el estado sin abrir detalles:")
    st.write("Préstamo A:", status_badge("activo"))
    st.write("Préstamo B:", status_badge("vencido"))
    st.write("Préstamo C:", status_badge("mora"))

    st.markdown("---")
    st.header("Proceso: Otorgar préstamo")
    steps = [
        ("Solicitud", "Llenado de datos y documentos"),
        ("Evaluación", "Revisión de promotora/directiva"),
        ("Aprobación", "Decisión en reunión"),
        ("Desembolso", "Entregar fondos al miembro"),
    ]
    stepper(current_step=2, steps=steps)
    st.markdown("Explicación: el stepper indica en qué paso está la solicitud y qué falta.")

    st.markdown("---")
    st.header("Progreso y checklist")
    st.write("Porcentaje del préstamo pagado:")
    progreso_bar(450, 1000, label="Pago acumulado")
    st.write("Checklist para cerrar ciclo (marca lo completado):")
    items = [{"key": "aportes", "label": "Todos los aportes registrados"},
             {"key": "actas", "label": "Actas firmadas"},
             {"key": "caja", "label": "Revisado saldo caja"}]
    res = checklist_cierre(items)
    st.write(res)

    st.markdown("---")
    st.header("Guía rápida interactiva")
    guided_tour(["Revisar miembros", "Registrar un aporte", "Generar reporte de cierre", "Validar actas"])

    st.markdown("---")
    st.header("Ayuda y recursos")
    st.write("Archivo ER (referencia de datos):")
    st.markdown(f"[Abrir ER de referencia](file:///mnt/data/ER proyecto - ER NUEVO.pdf)")

    st.markdown("---")
    st.info("Consejo: coloca esta página en el menú de ayuda/sobre para que nuevos usuarios la vean al ingresar.")
