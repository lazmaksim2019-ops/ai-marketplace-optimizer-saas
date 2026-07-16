import importlib.util
import sys
from pathlib import Path

_backend = str(Path(__file__).parent / "backend")
if _backend not in sys.path:
    sys.path.insert(0, _backend)

_spec = importlib.util.spec_from_file_location("_backend_main", Path(__file__).parent / "backend" / "main.py")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

app = _mod.app
