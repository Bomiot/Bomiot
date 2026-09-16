# Code Protection

## Introduction

Bomiot provides multi-layer Python code protection through compilation and hardening, raising the bar for source protection and reverse engineering — suitable for commercial distribution.

> Note: "Encryption" here refers to improving source protection and reverse-engineering difficulty through local compilation/packaging. Actual security depends on build strategy, obfuscation strength, and supplementary measures.

---

## Protection Layers

| Layer | Method | Use Case |
|-------|--------|----------|
| Project-level | Nuitka → single-file executable | Full distribution |
| Module-level | Nuitka → `.pyd`/`.so` | Core module protection |
| Critical path | PyO3 (Rust) for sensitive logic | Auth, license, payment |

---

## Project-Level Compilation

Compile the entire project into a single-file executable with `bomiot package`:

```bash
bomiot package my-project
```

Nuitka compiles Python to native binary, bundling runtime and dependencies — no exposed source or dependency tree.

---

## Module-Level Compilation

Compile core modules into binary extensions (`.pyd` on Windows / `.so` on Linux):

```bash
# Compile a specific module
python -m nuitka --module your_module.py
```

The compiled module can be imported by Python directly without source code.

---

## PyO3 (Rust) Hardening

For sensitive modules like auth, authorization, payment, and license verification, implement them in Rust (PyO3) and compile to extension modules to further raise reverse-engineering cost.

```rust
// lib.rs
use pyo3::prelude::*;

#[pyfunction]
fn verify_license(key: &str) -> bool {
    // License verification logic
    key.len() > 0
}

#[pymodule]
fn license_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(verify_license, m)?)?;
    Ok(())
}
```

```bash
# Compile to Python extension
maturin develop
```

---

## CI/CD Integration

Put compile/package steps into your CI pipeline:

```yaml
build:
  script:
    - bomiot package my-project
    - codesign dist/my-project.exe
    - upload-artifact dist/
```

Steps: build → binary signing → versioning → upload artifacts.

---

## Recommendations

1. **Layered protection**: Nuitka for general logic, Rust for sensitive logic
2. **Code signing**: Digitally sign binaries to prevent tampering
3. **Authorization**: Combine online/offline license checks
4. **Anti-debug**: Add anti-debugging and integrity checks
5. **Minimal exposure**: Distribute only necessary compiled artifacts

---

## Limitations

- Compilation raises reverse-engineering cost but does not guarantee absolute security
- Combine with authorization and anti-tampering measures
- Security strength depends on the overall build strategy, not a single tool
