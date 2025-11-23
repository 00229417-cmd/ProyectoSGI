# pega justo después de st.set_page_config(...) en app.py
st.markdown(
    """
    <style>
    /* Fondo degradado azul (full-screen) */
    .stApp {
        background: linear-gradient(180deg, #071032 0%, #0b2248 40%, #061426 100%);
        background-attachment: fixed;
    }

    /* Contenedor centralizado tipo card */
    .center-card {
        max-width: 1100px;
        margin: 18px auto 40px auto;
        padding: 28px;
        border-radius: 14px;
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        box-shadow: 0 10px 30px rgba(3,10,23,0.6);
        backdrop-filter: blur(6px) saturate(120%);
        border: 1px solid rgba(255,255,255,0.03);
    }

    /* header: avatar + title */
    .header-row {
        display:flex;
        align-items:center;
        gap:18px;
        margin-bottom:18px;
    }
    .avatar-g {
        width:72px;
        height:72px;
        border-radius:14px;
        display:flex;
        align-items:center;
        justify-content:center;
        font-weight:800;
        color:white;
        font-size:30px;
        background: linear-gradient(135deg,#5b8bff,#3c67d6);
        box-shadow: 0 14px 30px rgba(60,103,214,0.18);
        transform-origin:center;
        /* animación sutil (respiración) */
        animation: floaty 4.5s ease-in-out infinite;
    }

    @keyframes floaty {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-6px) scale(1.01); }
        100% { transform: translateY(0px); }
    }

    .header-title { color: #fff; margin: 0; font-size:28px; font-weight:700; }
    .header-sub { color: #9FB4D6; font-size:13px; margin-top:4px; }

    /* centrar contenido del form en la columna izquierda */
    .form-wrapper {
       padding-top: 6px;
    }

    /* expander custom */
    .stExpander {
        border-radius: 10px;
    }

    /* ajustar inputs (no touch heavy styling to keep streamlit native look) */
    .stTextInput > label, .stNumberInput > label {
        color: #C9D8EE;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# Header HTML (render)
st.markdown(
    """
    <div class="center-card">
      <div class="header-row">
        <div class="avatar-g">G</div>
        <div>
          <div class="header-title">GAPC — Portal</div>
          <div class="header-sub">Sistema de Gestión para Grupos de Ahorro y Préstamo Comunitarios</div>
        </div>
      </div>
    """,
    unsafe_allow_html=True,
)
# ... después de que tu app muestre el login y demás, recuerda cerrar el div:
# st.markdown("</div>", unsafe_allow_html=True)





