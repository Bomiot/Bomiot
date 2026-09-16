# 代码保护

## 简介

Bomiot 提供多层次的 Python 代码保护方案，通过编译与加固提高源码保护与逆向难度，适合商业化分发。

> 注意：术语「加密」在此指通过本地化编译/打包提高源码保护与逆向难度。实际安全性取决于构建策略、混淆强度与补充的安全措施。

---

## 保护层次

| 层次 | 方式 | 适用场景 |
|------|------|----------|
| 项目级编译 | Nuitka 编译为单文件可执行程序 | 整体分发 |
| 模块级编译 | Nuitka 编译指定模块为 `.pyd`/`.so` | 核心模块保护 |
| 关键路径加固 | PyO3（Rust）实现敏感逻辑 | 认证、授权、支付等 |

---

## 项目级编译

通过 `bomiot package` 将整个项目编译为单文件可执行程序：

```bash
bomiot package my-project
```

该过程使用 Nuitka 将 Python 代码编译为本地二进制，运行时与依赖一并打包，避免裸露源码与依赖树。

---

## 模块级编译

对核心模块单独编译为二进制扩展（`.pyd` on Windows / `.so` on Linux）：

```bash
# 编译指定模块
python -m nuitka --module your_module.py
```

编译后的模块可直接被 Python import，无需源码即可运行。

---

## PyO3（Rust）加固

对认证、授权、支付、许可证验证等敏感模块，推荐使用 Rust（PyO3）实现并编译为扩展模块，进一步提高逆向成本。

```rust
// lib.rs
use pyo3::prelude::*;

#[pyfunction]
fn verify_license(key: &str) -> bool {
    // 许可证验证逻辑
    key.len() > 0
}

#[pymodule]
fn license_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(verify_license, m)?)?;
    Ok(())
}
```

```bash
# 编译为 Python 扩展
maturin develop
```

---

## CI/CD 集成

建议将编译/打包步骤放入 CI 流程：

```yaml
# 伪代码
build:
  script:
    - bomiot package my-project
    - codesign dist/my-project.exe   # 代码签名
    - upload-artifact dist/
```

步骤：构建 → 二进制签名 → 版本化 → 上传 Artifacts。

---

## 建议

1. **分层保护**：普通逻辑用 Nuitka 编译，敏感逻辑用 Rust 实现
2. **代码签名**：对二进制进行数字签名，防止篡改
3. **授权验证**：结合在线/离线授权机制，防止未经授权分发
4. **反调试**：可加入反调试、完整性校验等措施
5. **最小暴露**：仅分发必要的编译产物，不包含源码

---

## 局限性

- 编译提高逆向成本，但不能保证绝对安全
- 建议结合授权验证、反篡改等补充措施
- 安全强度取决于整体构建策略，而非单一工具
