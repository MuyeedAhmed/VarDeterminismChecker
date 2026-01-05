import importlib
import importlib.util
import inspect
import os
from types import ModuleType
from typing import Any
from typing import Optional

def ModuleFile(modname: str) -> Optional[str]:
    spec = importlib.util.find_spec(modname)
    if spec is None:
        return None
    return spec.origin

def _import_module(modname: str) -> ModuleType:
    return importlib.import_module(modname)

def ResolveAttrChain(obj: Any, attrs: list[str]) -> Any:
    for a in attrs:
        obj = getattr(obj, a)
    return obj

def ResolveSourcePath(dotted: str) -> str:
    dotted = dotted.strip()

    f = ModuleFile(dotted)
    if f:
        return os.path.abspath(f)
    parts = dotted.split(".")
    for i in range(len(parts), 0, -1):
        modname = ".".join(parts[:i])
        attr_chain = parts[i:]
        try:
            mod = _import_module(modname)
        except Exception:
            continue

        if not attr_chain:
            f = ModuleFile(modname)
            if f:
                return os.path.abspath(f)
            break

        try:
            obj = ResolveAttrChain(mod, attr_chain)
        except AttributeError:
            continue
        f = inspect.getsourcefile(obj) or inspect.getfile(obj)
        if f:
            return os.path.abspath(f)

    raise FileNotFoundError(f"Could not resolve '{dotted}' to a source file.")

# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) < 2:
#         print("Errror: \nFormat: python resolve.py lib\n")
#         return None
#     print(resolve_source_path(sys.argv[1]))
    