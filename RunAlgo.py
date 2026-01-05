import importlib
import inspect
import itertools
import numpy as np
import sys

TEST_INPUTS = [0, 1, -1, 1.5, None, "x", [1, 2, 3], np.array([1, 2, 3])]

def PositionalArity(fn):
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):
        return None, None, False

    params = list(sig.parameters.values())
    has_varargs = any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in params)

    pos = [
        p for p in params
        if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    ]
    min_args = sum(1 for p in pos if p.default is inspect._empty)
    max_args = None if has_varargs else len(pos)
    return min_args, max_args, has_varargs

def Probe(func_path, max_arity_if_unknown = 3):
    mod, name = func_path.rsplit(".", 1)
    fn = getattr(importlib.import_module(mod), name)
    if not callable(fn):
        raise TypeError(f"{func_path} is not callable")
    
    min_args, max_args, has_varargs = PositionalArity(fn)

    if min_args is None:
        arities = range(1, max_arity_if_unknown + 1)
    else:
        if max_args is None:
            arities = range(min_args, min(min_args + 2, max_arity_if_unknown) + 1)
        else:
            arities = range(min_args, max_args + 1)

    for arity in arities:
        for args in itertools.product(TEST_INPUTS, repeat=arity):
            try:
                fn(*args)
                print(f"Successful Argument: {args}")
                return
            except Exception as e:
                pass
                # print(f"FAIL args={args} -> {type(e).__name__}: {e}")

    print(f"Failed to run {func_path} with any argument combination of arities {list(arities)}")
        
if __name__ == "__main__":
    # probe("numpy.bartlett")
    # probe("scipy.stats.zscore")
    # Probe("numpy.random.normal")
    args = sys.argv
    libFunction = args[1]
    Probe(libFunction)
