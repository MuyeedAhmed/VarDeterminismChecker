# Variable Determinism Checker (Python)

This tool analyzes **library functions** to determine which **variables are deterministic or nondeterministic**.  
It combines **AST-based static analysis** with **dynamic execution tracing** to compare variable behavior across multiple runs.

---

## Features

- Identifies deterministic vs. nondeterministic variables in a function
- Uses **two executions** to detect nondeterminism
- Outputs detailed traces for post-analysis

---

## Usage

Run the tool using:

```bash
./RunTND <module.function>
```

### Example

```bash
./RunTND numpy.bartlett
```

---

## Output

All results are written to the `TraceOutput/` directory.

Each variable is associated with a **determinism label**:

| Value | Meaning |
|------:|---------|
| `0` | Nondeterministic |
| `1` | Deterministic |
| `2` | Comparison failed between executions |

A value of `2` typically indicates that the tool could not reliably compare the variable across the two runs (e.g., unsupported type).

