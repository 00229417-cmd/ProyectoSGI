# modulos/login.py  (poner exactamente en modulos/login.py)
import streamlit as st

def login_page():
    st.title("Login - prueba")
    st.write("Si ves esto, el módulo modulos.login se importó correctamente.")

# Permite ejecución directa para debug local
if __name__ == "__main__":
    import streamlit as st
    login_page()

