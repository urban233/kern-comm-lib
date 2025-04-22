# Kern - Common Python Libraries
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

The repository contains the Kern Python library code. 
Kern (`kern-comm-lib`) is an open-source collection of Python code designed to augment the Python standard library.
It provides robust, exception-free Python utilities for building reliable applications
and features modern error handling with `Status` and `StatusOr` to eliminate runtime surprises.
<p align="center">
    <img alt="Kern Logo" src="assets/logo_wide.png"  width="600"/>
</p>

[**Features**](#features) | [**Installation**](#installation) | [**License**](#license)

> [!IMPORTANT]  
> 📣 **Kern-comm-lib is under active development.**  
> APIs will (greatly) evolve until v1.0.

## Features ✨  
- **Exception-Free Modules**: Predictable error handling without `try/except` sprawl.  
- **Status & StatusOr**: Modern result types for explicit success/failure handling.
- **Thread-safe Logging**: Log messages with thread safety and flexibility.

## Installation ⚙️  
```bash
pip install kern-comm-lib
```

## Design Philosophy
The core idea of Kern is to provide an exception-free alternative to common
standard libraries of Python. Kern is divided into two major parts: (1) the 
`base` package and (2) other high-level packages (e.g. filesystem). 
The `base` package is the standard every other high-level package uses. For 
example, the `base` package contains the `log` and `status` package which 
should be used in a high-level package like `filesystem` that wraps filesystem
functions of the standard library in an exception-free way. Therefore, the
high-level packages are consumers of the `base` package and should it import 
like any other user with `import kern_comm_lib as kern`.

## Contributing 🤝
Contributions are welcome! 
Be aware that this project uses ruff as a linter pyink as a formatter,
and pyright as a type checker.

## License 📜
BSD-3 Clause. See [LICENSE](LICENSE).

---

*Engineered for reliability.*
