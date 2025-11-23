# Ejemplo muy simple
def calcular_cuotas_simples(monto, plazo_meses):
    monto = float(monto)
    plazo = int(plazo_meses)
    if plazo <= 0:
        raise ValueError("plazo_meses debe ser mayor a 0")
    cuota = round(monto / plazo, 2)
    return [cuota for _ in range(plazo)]
