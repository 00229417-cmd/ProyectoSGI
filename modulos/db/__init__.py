# modulos/db/__init__.py
import importlib
import pkgutil
import sys
from pathlib import Path

# Auto-import modules presentes en el directorio modulos/db
# Esto evita que la importación falle si algún CRUD no existe.
base = Path(__file__).parent
for finder, name, ispkg in pkgutil.iter_modules([str(base)]):
    try:
        module = importlib.import_module(f"modulos.db.{name}")
        globals()[name] = module
    except Exception:
        # no romper la importación general si algún archivo tiene errores
        pass

__all__ = [name for _, name, _ in pkgutil.iter_modules([str(base)])]

