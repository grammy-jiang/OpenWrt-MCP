<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Project Dependencies & Environment Management](#project-dependencies--environment-management)
  - [1. Environment Management](#1-environment-management)
    - [Workflow](#workflow)
  - [2. Core Dependencies](#2-core-dependencies)
    - [MCP Framework](#mcp-framework)
    - [Database & ORM](#database--orm)
    - [Networking (HTTP/Ubus)](#networking-httpubus)
    - [Networking (SSH Fallback)](#networking-ssh-fallback)
    - [Utilities](#utilities)
  - [3. Dependency Groups](#3-dependency-groups)
    - [Group: `test`](#group-test)
    - [Group: `lint`](#group-lint)
    - [Group: `dev`](#group-dev)
  - [4. Proposed `pyproject.toml` Configuration](#4-proposed-pyprojecttoml-configuration)
  - [5. Code Quality Automation](#5-code-quality-automation)
  - [6. Usage Cheat Sheet](#6-usage-cheat-sheet)
    - [Development Quick Start](#development-quick-start)
    - [Managing Dependencies](#managing-dependencies)
    - [Running Commands](#running-commands)
    - [Code Quality (Pre-commit)](#code-quality-pre-commit)
    - [Packaging & Publishing](#packaging--publishing)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

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
- **`pre-commit`**: Framework for managing and maintaining multi-language pre-commit hooks.

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
    "pre-commit",
]
```

## 5. Code Quality Automation

We will use **pre-commit** to ensure code quality standards are enforced before every commit.

- **Configuration**: `.pre-commit-config.yaml`
- **Hooks**:
  - `ruff`: For linting and formatting.
  - `mypy`: For static type checking.
  - `check-yaml`: Validates YAML files.
  - `check-toml`: Validates TOML files.
  - `end-of-file-fixer`: Ensures files end with a newline.
  - `trailing-whitespace`: Trims trailing whitespace.

## 6. Usage Cheat Sheet

### Development Quick Start

1. **Install dependencies:**

   ```bash
   uv sync
   ```

1. **Install pre-commit hooks:**

   ```bash
   uv run --group lint pre-commit install
   ```

1. **Run the server:**

   ```bash
   uv run openwrt-mcp
   ```

1. **Run tests:**

   ```bash
   uv run pytest
   ```

1. **Run code quality checks:**

   ```bash
   uv run --group lint pre-commit run --all-files
   ```

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

- **Update all dependencies:**

  ```bash
  uv lock --upgrade
  ```

- **Update a specific dependency:**

  ```bash
  uv lock --upgrade-package httpx
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

### Code Quality (Pre-commit)

- **Install pre-commit hooks (run once):**

  ```bash
  uv run --group lint pre-commit install
  ```

- **Run hooks manually on all files:**

  ```bash
  uv run --group lint pre-commit run --all-files
  ```

- **Update pre-commit hooks:**

  ```bash
  uv run --group lint pre-commit autoupdate
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
