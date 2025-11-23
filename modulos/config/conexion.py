from sqlalchemy import text

def test_connection():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            r = result.scalar()
            return True, f"Conexión OK (SELECT 1 -> {r})"
    except OperationalError as e:
        return False, f"Error de conexión: {e}"
    except Exception as e:
        return False, f"Error inesperado: {e}"

