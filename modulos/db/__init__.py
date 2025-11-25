# modulos/db/__init__.py
import importlib

__all__ = []

crud_modules = [
    "crud_miembros", "crud_ahorro", "crud_aporte", "crud_prestamo",
    "crud_cuota", "crud_caja", "crud_reunion", "crud_asistencia",
    "crud_multa", "crud_cierre", "crud_promotora", "crud_grupo",
    "crud_ciclo", "crud_reporte", "crud_users"
]

for name in crud_modules:
    try:
        module = importlib.import_module(f"modulos.db.{name}")
        globals()[name] = module
        __all__.append(name)
    except Exception:
        pass

