# Kern - Common Python Libraries · [![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
The repository contains the Kern Python library code. 
Kern (kern-comm-lib) is an open-source collection of Python code designed to augment the Python standard library.
It provides robust, exception-free Python utilities for building reliable applications
and features modern error handling with `Status` and `StatusOr` to eliminate runtime surprises.
<p align="center">
    <img alt="Kern Logo" src="assets/logo.png"  width="200"/>
</p>

[**Overview**](#overview) | [**Features**](#features) | [**Installation**](#installation) | [**Quick Start**](#quick-start) | [**Why Kern?**](#why-kern) | [**License**](#license)

> [!IMPORTANT]  
> 📣 **Kern-comm-lib is under active development.**  
> APIs will (greatly) evolve until v1.0.

## Features ✨  
- **Exception-Free Modules**: Predictable error handling without `try/except` sprawl.  
- **Status & StatusOr**: Modern result types for explicit success/failure handling.

## Installation ⚙️  
```bash
pip install kern-comm-lib
```

## Quick Start 🚀
### Using `Status` and `StatusOr`
```python
import kern_comm_lib as kern

# Example 1: Status for void functions
def create_dir(path: str) -> kern.Status:
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            return kern.Status.OK()
        except OSError as e:
            return kern.Status.ERROR(f"Failed: {e}")
    return kern.Status.OK()

result = create_dir("/data/logs")
if not result.ok:
    print(result.message)  # Explicit error handling

# Example 2: StatusOr for returning values
def parse_config(file: str) -> kern.StatusOr[dict]:
    try:
        with open(file, "r") as f:
            data = yaml.safe_load(f)
            return kern.StatusOr(data)
    except (FileNotFoundError, yaml.YAMLError) as e:
        return kern.StatusOr.ERROR(f"Config error: {e}")

config_result = parse_config("settings.yaml")
if config_result.ok:
    setup(config_result.value)  # Safe access to value
else:
    handle_error(config_result.error)
```

## Why "Kern"? ❓
The name *Kern* (German/Dutch for **"core"**) reflects this library’s focus on **foundational, reliable utilities**. It is **not** related to typography ("kerning") or OS kernels.

## License 📜
BSD-3 Clause. See [LICENSE](LICENSE).

---

*Engineered for reliability.*
