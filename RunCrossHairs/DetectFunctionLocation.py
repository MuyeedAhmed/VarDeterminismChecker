import importlib
import inspect
import os
import shutil
from RunAlgo import Probe

def load_function(qualname: str):
    modname, funcname = qualname.rsplit(".", 1)
    module = importlib.import_module(modname)
    func = getattr(module, funcname)
    return module, func

def get_source_info(func):
    info = {}
    try:
        info["source_file"] = inspect.getsourcefile(func)
        info["source_lines"], info["line_no"] = inspect.getsourcelines(func)
    except (OSError, TypeError):
        info["source_file"] = inspect.getfile(func)
        info["source_lines"] = None
        info["line_no"] = None

    info["module"] = func.__module__
    info["qualname"] = func.__qualname__
    return info


def get_signature(func):
    try:
        return inspect.signature(func)
    except ValueError:
        return None

import numpy as np



def _contains_ndarray(x, max_nodes=2000):
    seen = set()
    stack = [x]
    steps = 0
    while stack and steps < max_nodes:
        steps += 1
        v = stack.pop()
        vid = id(v)
        if vid in seen:
            continue
        seen.add(vid)

        if isinstance(v, np.ndarray):
            return True
        if isinstance(v, np.generic):
            continue
        if isinstance(v, tuple) or isinstance(v, list):
            stack.extend(v)
            continue
        if isinstance(v, dict):
            stack.extend(v.values())
            continue
    return False


def emit_determinism_assert(qualname, signature, out):
    lines = []
    call = f"{qualname}{signature}"

    if isinstance(out,  (type(None), bool, int, float, complex, str, bytes, bytearray)) or isinstance(out, np.generic):
        lines.append(f"    assert {call} == {call}")
        return lines

    if isinstance(out, np.ndarray):
        lines.append(f"    assert np.array_equal({call}, {call})")
        return lines

    if isinstance(out, tuple):
        if _contains_ndarray(out):
            lines.append(f"    _a = {call}")
            lines.append(f"    _b = {call}")
            lines.append("    assert len(_a) == len(_b)")
            lines.append("    assert all(np.array_equal(x, y) if isinstance(x, np.ndarray) else x == y for x, y in zip(_a, _b))")
        else:
            lines.append(f"    assert {call} == {call}")
        return lines

    if isinstance(out, list):
        if _contains_ndarray(out):
            lines.append(f"    _a = {call}")
            lines.append(f"    _b = {call}")
            lines.append("    assert len(_a) == len(_b)")
            lines.append("    assert all(np.array_equal(x, y) if isinstance(x, np.ndarray) else x == y for x, y in zip(_a, _b))")
        else:
            lines.append(f"    assert {call} == {call}")
        return lines

    if isinstance(out, dict):
        if _contains_ndarray(out):
            lines.append(f"    _a = {call}")
            lines.append(f"    _b = {call}")
            lines.append("    assert _a.keys() == _b.keys()")
            lines.append("    assert all(np.array_equal(_a[k], _b[k]) if isinstance(_a[k], np.ndarray) else _a[k] == _b[k] for k in _a)")
        else:
            lines.append(f"    assert {call} == {call}")
        return lines

    lines.append(f"    assert repr({call}) == repr({call})")
    return lines
    


def WriteCrossHairMarker(file, FilePath, qualname, signature, line_no, functionOutput):
    file.write(f"def CrosshairWrapper{signature}:\n")
    determinism_asserts = emit_determinism_assert(qualname, signature, functionOutput)
    for assert_line in determinism_asserts:
        file.write(f"{assert_line}\n")
    file.write("\n")

def ModifyLibFile(FilePath, qualname, signature, startLine, functionOutput):
    OriginalCodeTemporaryPath = FilePath[:-3]+"_Original.py"
    OutputFilePath = FilePath[:-3]+"_Output.py"
    print("Modifying", FilePath)

    if os.path.exists(OriginalCodeTemporaryPath) == 0:
        shutil.copy(FilePath, OriginalCodeTemporaryPath)
    source_code = ""
    with open(FilePath, 'r') as file:
        source_code = file.read()
    
    OrginalFile = open(OriginalCodeTemporaryPath, 'r')
    OrginalFileLines = OrginalFile.readlines()
    OFLines = iter(OrginalFileLines)
    
    line_counter = 0
    
    with open(OutputFilePath, 'w') as file:
        for line in OFLines:
            line_counter += 1
            if line_counter == startLine:
                print("start")
                WriteCrossHairMarker(file, FilePath, qualname, signature, line_no, functionOutput)
            file.write(line)

    os.remove(FilePath)
    os.rename(OutputFilePath, FilePath)

def reset(FilePath, OriginalCodeTemporaryPath):
    os.remove(FilePath)
    os.rename(OriginalCodeTemporaryPath, FilePath)


# libFunc = "numpy.bartlett"
libFunc = "numpy.blackman"

# libFunc = "numpy.linalg.svd"

module, func = load_function(libFunc)
sourceInfo = get_source_info(func)

out = Probe(libFunc)

filePath = sourceInfo["source_file"]
qualname = sourceInfo["qualname"]
line_no = sourceInfo["line_no"]
signature = get_signature(func)

ModifyLibFile(filePath, qualname, signature, line_no, out)

