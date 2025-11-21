# Project Dependencies & Environment Management

This document outlines the technical stack and dependency management strategy for the OpenWrt MCP Server, utilizing `uv` as the package manager.

## 1. Environment Management

We will use **[uv](https://github.com/astral-sh/uv)** for Python project management. It handles python versions, virtual environments, and dependency resolution with extreme speed.

### Workflow

- **Initialization**: `uv init`
- **Adding Dependencies**: `uv add <package>`
- **Running Dev Server**: `uv run fastmcp dev main.py`
- **Lockfile**: `uv.lock` ensures reproducible builds.

## 2. Core Dependencies

### MCP Framework

- **Library**: `fastmcp`
- **Purpose**: Provides the high-level API to define tools and resources easily. It simplifies the MCP protocol implementation.
- **Why**: The user explicitly requested FastMCP in the design phase.

### Database & ORM

- **Library**: `sqlmodel` (wraps SQLAlchemy + Pydantic)
- **Purpose**: Manages the SQLite database for the Device Registry (`devices.db`).
- **Why**: Combines the validation of Pydantic with the ORM capabilities of SQLAlchemy, perfect for modern Python apps.

### Networking (HTTP/Ubus)

- **Library**: `httpx`
- **Purpose**: Handling JSON-RPC requests to the OpenWrt `ubus` endpoint.
- **Why**: Supports **async/await**, which is crucial for keeping the MCP server responsive while waiting for network I/O. It is a modern replacement for `requests`.

### Networking (SSH Fallback)

- **Library**: `asyncssh` (or `paramiko`)
- **Recommendation**: `asyncssh`
- **Purpose**: Executing commands that Ubus cannot handle (e.g., `sysupgrade`, complex shell scripts).
- **Why**: Since `fastmcp` and `httpx` are async, using an async SSH library prevents blocking the event loop.

### Utilities

- **`pydantic`**: Data validation (transitive dependency of SQLModel/FastMCP).
- **`python-dotenv`**: Managing local development secrets (optional, if we need `.env` for global settings).

## 3. Dependency Groups

We will organize development dependencies into specific groups to keep the environment clean and allow for targeted installation/execution.

### Group: `test`

- **`pytest`**: The standard testing framework.
- **`pytest-asyncio`**: Essential for testing our async `httpx` and `asyncssh` code.
- **`pytest-cov`**: For measuring code coverage.

### Group: `lint`

- **`ruff`**: An extremely fast Python linter and formatter. Replaces `black`, `isort`, and `flake8`.
- **`mypy`**: Static type checker to ensure our Pydantic models and async logic are type-safe.

### Group: `dev`

- **`python-dotenv`**: For loading environment variables from `.env` during local development.
- **`ipython`**: (Optional) For interactive debugging and exploration.

## 4. Proposed `pyproject.toml` Configuration

We will use the standard `[dependency-groups]` table (PEP 735) supported by `uv`.

```toml
[project]
name = "openwrt-mcp"
version = "0.1.0"
description = "MCP Server for OpenWrt router management"
requires-python = ">=3.10"
dependencies = [
    "fastmcp",
    "sqlmodel",
    "httpx",
    "asyncssh",
]

[dependency-groups]
dev = [
    "python-dotenv",
    "ipython",
]
test = [
    "pytest",
    "pytest-asyncio",
    "pytest-cov",
]
lint = [
    "ruff",
    "mypy",
]
```

## 5. Usage Cheat Sheet

This section serves as a quick reference for common `uv` commands used in this project.

### Managing Dependencies

- **Add a core dependency:**

  ```bash
  uv add httpx
  ```

- **Add a development dependency (to `dev` group):**

  ```bash
  uv add --group dev ipython
  ```

- **Add a test dependency (to `test` group):**

  ```bash
  uv add --group test pytest
  ```

- **Remove a dependency:**

  ```bash
  uv remove httpx
  ```

- **Sync environment (install all dependencies from lockfile):**
  ```bash
  uv sync --all-groups
  ```

### Running Commands

- **Run the MCP Server (Development Mode):**

  ```bash
  uv run fastmcp dev main.py
  ```

- **Run a Python script in the environment:**

  ```bash
  uv run python scripts/setup_db.py
  ```

- **Run Tests:**

  ```bash
  uv run --group test pytest
  ```

- **Run Linter (Ruff):**

  ```bash
  uv run --group lint ruff check .
  ```

- **Run Type Checker (MyPy):**

  ```bash
  uv run --group lint mypy .
  ```

- **Open a REPL with dependencies loaded:**
  ```bash
  uv run --group dev ipython
  ```

### Packaging & Publishing

- **Build the project (Source and Wheel):**

  ```bash
  uv build
  ```

- **Publish to PyPI:**

  ```bash
  uv publish
  ```

- **Publish to a custom repository (e.g., TestPyPI):**
  ```bash
  uv publish --publish-url https://test.pypi.org/legacy/
  ```
