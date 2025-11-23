<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [OpenWrt-MCP Coding Agent Instructions](#openwrt-mcp-coding-agent-instructions)
  - [Repository Overview](#repository-overview)
  - [Critical Build Requirements](#critical-build-requirements)
    - [Environment Setup](#environment-setup)
    - [Build and Run Commands](#build-and-run-commands)
    - [Code Quality and Linting](#code-quality-and-linting)
  - [Project Architecture](#project-architecture)
    - [Directory Structure](#directory-structure)
    - [Key Architectural Components](#key-architectural-components)
    - [Important Configuration Files](#important-configuration-files)
  - [Dependency Management](#dependency-management)
  - [Testing Strategy](#testing-strategy)
  - [Common Pitfalls and Workarounds](#common-pitfalls-and-workarounds)
  - [Making Code Changes](#making-code-changes)
    - [Step-by-Step Workflow](#step-by-step-workflow)
    - [Component-Specific Guidelines](#component-specific-guidelines)
  - [Design Documentation](#design-documentation)
  - [Trusting These Instructions](#trusting-these-instructions)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# OpenWrt-MCP Coding Agent Instructions

## Repository Overview

**OpenWrt-MCP** is a production-minded MCP (Model Context Protocol) server for OpenWrt routers, built with Python 3.13+ and FastMCP. It provides guardrailed tools for UCI/ubus operations, service control (dnsmasq, firewall4, hostapd), system facts, and health/telemetry collection. The goal is to enable reproducible, auditable network operations for single routers or entire fleets.

**Repository Statistics:**

- **Primary Language:** Python 3.13
- **Package Manager:** `uv` (modern, fast Python package manager)
- **Framework:** FastMCP 2.13.1
- **Source Lines:** ~800 lines of Python code
- **Project Structure:** `src`-layout with modular architecture
- **Dependencies:** asyncssh, fastmcp, httpx, sqlmodel
- **Database:** SQLite for device registry

**Development Status:** Early stage (Stage 1 MVP planned, features in development)

## Critical Build Requirements

### Environment Setup

**ALWAYS use `uv` for all Python operations.** This project uses `uv` (version 0.9.11+) as the package manager, NOT pip, pipenv, or poetry.

1. **Install uv (if not available):**

   ```bash
   pip install uv
   ```

1. **Initial Setup - ALWAYS run first:**

   ```bash
   uv sync --all-groups
   ```

   - This installs all dependencies including dev, test, and lint groups
   - Takes approximately 60-90 seconds on first run
   - Creates a `.venv` virtual environment automatically

### Build and Run Commands

**Running the application:**

```bash
# Standard mode (STDIO transport)
uv run openwrt-mcp

# SSE transport mode
uv run openwrt-mcp --transport sse --host 0.0.0.0 --port 8000
```

- The server starts successfully and displays the FastMCP banner
- Use Ctrl+C to stop the server

**Building the package:**

```bash
uv build
```

- Creates distribution files in `dist/` directory
- Produces both `.tar.gz` and `.whl` files
- Takes ~10 seconds

**Testing:**

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=src/openwrt_mcp --cov-report=term
```

- All 6 unit tests should pass
- Test execution takes ~0.1 seconds
- Current coverage: ~31% (focused on device_manager)

### Code Quality and Linting

**ALWAYS run pre-commit hooks before finalizing changes:**

1. **First time only - install hooks:**

   ```bash
   uv run --group lint pre-commit install
   ```

1. **Run all checks (REQUIRED before commit):**

   ```bash
   uv run --group lint pre-commit run --all-files
   ```

   - Takes 60-120 seconds on first run (downloads hook environments)
   - Subsequent runs take ~10-15 seconds
   - All checks must pass before committing

**Individual linting commands:**

```bash
# Python linting with ruff
uv run --group lint ruff check .

# Python formatting with ruff
uv run --group lint ruff format .

# Type checking with mypy
uv run --group lint mypy .

# Markdown linting
uv run --group lint pre-commit run markdownlint --all-files

# YAML linting
uv run --group lint pre-commit run yamllint --all-files
```

**Pre-commit hooks include:**

- File checks (large files, merge conflicts, shebangs, symlinks)
- YAML validation
- End-of-file fixer
- Trailing whitespace removal
- uv.lock synchronization check
- Markdown: doctoc (TOC generation), markdownlint, proselint
- Shell: bashate, shellcheck
- Python: ruff (lint + format), mypy
- YAML: yamlfmt, yamllint

## Project Architecture

### Directory Structure

```text
/
├── .github/                    # GitHub configuration (you're adding copilot-instructions.md here)
├── .pre-commit-config.yaml     # Pre-commit hooks configuration
├── .python-version             # Python version: 3.13
├── pyproject.toml              # Project metadata, dependencies, build config
├── uv.lock                     # Dependency lockfile (DON'T edit manually)
├── main.py                     # Legacy entry point (minimal, use openwrt-mcp command)
├── README.md                   # Project documentation
├── design/                     # Design documents (9 files, ~1000 lines)
│   ├── dependencies.md         # Detailed dependency and uv usage guide
│   ├── project_structure.md    # Architecture overview
│   ├── feature_spec_stage1.md  # Stage 1 MVP specifications
│   ├── feature_spec_stage2.md  # Stage 2 advanced features
│   ├── feature_spec_stage3.md  # Stage 3 professional tools
│   └── (others)                # Other design docs
├── src/openwrt_mcp/            # Main package (src-layout)
│   ├── __init__.py             # Package version: 0.1.0
│   ├── __main__.py             # CLI entry point (36 lines)
│   ├── server.py               # FastMCP server initialization (28 lines)
│   ├── config.py               # Configuration management (33 lines)
│   ├── exceptions.py           # Custom exceptions (40 lines)
│   ├── db/                     # Database layer
│   │   ├── engine.py           # SQLite engine setup
│   │   └── models.py           # Device model (SQLModel)
│   ├── managers/               # Business logic
│   │   ├── device_manager.py   # Device registry CRUD (67 lines, 96% coverage)
│   │   └── connection_manager.py  # HTTP/SSH connection pooling (32 lines)
│   ├── tools/                  # MCP tool definitions
│   │   ├── registry.py         # Device management tools (49 lines)
│   │   ├── system.py           # System health tools (38 lines)
│   │   ├── network.py          # Network interface tools (24 lines)
│   │   └── uci.py              # UCI configuration tools (58 lines)
│   └── utils/                  # Protocol adapters
│       ├── ubus.py             # Ubus JSON-RPC client (76 lines)
│       ├── ssh.py              # Async SSH wrapper (38 lines)
│       └── parsers.py          # CLI output parsers (17 lines)
└── tests/                      # Test suite
    ├── conftest.py             # Pytest fixtures (in-memory DB)
    └── unit/
        └── test_device_manager.py  # 6 tests, all passing
```

### Key Architectural Components

1. **Entry Point (`__main__.py`):** Parses CLI arguments (transport, host, port), initializes and runs the FastMCP server, supports both STDIO and SSE transports

1. **Server (`server.py`):** Initializes database with `init_db()`, creates `DeviceManager` and `ConnectionManager` instances, registers all tool modules (registry, system, network, UCI), exports `mcp` FastMCP instance

1. **Database Layer (`db/`):** Uses SQLite at `~/.config/openwrt-mcp/devices.db`, single `Device` model with fields: name (PK), host, username, password, protocol, port, SQLModel ORM (combines SQLAlchemy + Pydantic)

1. **Managers (`managers/`):** DeviceManager provides CRUD operations for device registry (well-tested), ConnectionManager handles HTTP/SSH session pooling (minimal implementation)

1. **Tools (`tools/`):** FastMCP tool definitions grouped by domain, purely declarative and delegates to managers, validates inputs with Pydantic via FastMCP

1. **Utils (`utils/`):** Protocol adapters for Ubus JSON-RPC and SSH, CLI output parsers (for Stage 2/3 features)

### Important Configuration Files

- **pyproject.toml:** Project metadata, dependencies in groups (dev, test, lint), build config
- **.pre-commit-config.yaml:** 11 repos with hooks for Python, Markdown, Shell, YAML
- **.mdlrc + .mdl_style.rb:** Markdownlint configuration
- **.proselintrc.json:** Prose linting config (disables some typography checks)
- **.gitignore:** Comprehensive (generated from toptal.com for Python, editors, OSes)

## Dependency Management

**Adding dependencies:**

```bash
# Core dependency
uv add <package>

# Dev dependency
uv add --group dev <package>

# Test dependency
uv add --group test <package>

# Lint dependency
uv add --group lint <package>
```

**ALWAYS run `uv sync --all-groups` after:**

- Pulling changes that modify `pyproject.toml` or `uv.lock`
- Adding or removing dependencies
- Switching branches

**The `uv.lock` file is automatically maintained and should be committed.**

## Testing Strategy

**Test Location:** All tests in `tests/` directory

- `conftest.py`: Shared fixtures (in-memory SQLite database)
- `unit/test_device_manager.py`: Device registry CRUD tests (6 tests)

**Writing Tests:**

- Use pytest with asyncio support (`pytest-asyncio` installed)
- Use fixtures from `conftest.py`: `session`, `device_manager`
- Follow existing test patterns (see `test_device_manager.py`)

**Test Coverage:**

- Current: 31% overall (device_manager: 96%)
- Run coverage: `uv run pytest --cov=src/openwrt_mcp`
- Untested areas: tools, utils, server initialization (acceptable for early stage)

## Common Pitfalls and Workarounds

1. **DON'T use `pip install` or `pip` commands directly** - always use `uv`
1. **DON'T edit `uv.lock` manually** - it's automatically managed
1. **DON'T skip `uv sync --all-groups`** - missing dev dependencies will break linting/testing
1. **ALWAYS run pre-commit before committing** - saves time in CI (when added)
1. **Pre-commit first run is slow (~120s)** - subsequent runs are fast (~10s)
1. **Python version:** Must be 3.13+ (specified in `.python-version` and `pyproject.toml`)

## Making Code Changes

### Step-by-Step Workflow

1. **Initial setup (if fresh clone):**

   ```bash
   uv sync --all-groups
   uv run --group lint pre-commit install
   ```

1. **Before making changes:**

   ```bash
   # Verify tests pass
   uv run pytest -v

   # Verify linting passes
   uv run --group lint ruff check .
   uv run --group lint mypy .
   ```

1. **Make your changes** to relevant files

1. **Test your changes iteratively:**

   ```bash
   # Run specific test
   uv run pytest tests/unit/test_device_manager.py -v

   # Run all tests
   uv run pytest -v
   ```

1. **Lint your changes:**

   ```bash
   # Auto-fix issues
   uv run --group lint ruff check --fix .
   uv run --group lint ruff format .

   # Type check
   uv run --group lint mypy .
   ```

1. **Run full pre-commit check:**

   ```bash
   uv run --group lint pre-commit run --all-files
   ```

1. **Verify the application still runs:**

   ```bash
   uv run openwrt-mcp
   # Should see FastMCP banner, press Ctrl+C to stop
   ```

### Component-Specific Guidelines

**Adding a new tool (in `tools/`):**

- Follow existing patterns in `registry.py`, `system.py`, etc.
- Use FastMCP decorators (`@mcp.tool()`)
- Delegate business logic to managers
- Return human-readable strings or structured JSON
- Register tool in `tools/__init__.py` and `server.py`

**Adding database models (in `db/models.py`):**

- Use SQLModel (not plain SQLAlchemy or Pydantic)
- Include `table=True` in model config
- Run tests to ensure migrations work with in-memory DB

**Adding utilities (in `utils/`):**

- Keep protocol-agnostic and reusable
- Add type hints for mypy compliance
- Consider adding unit tests if complex logic

**Modifying managers (in `managers/`):**

- These are well-tested (device_manager: 96% coverage)
- Run existing tests after changes
- Add new tests for new methods

## Design Documentation

The `design/` directory contains comprehensive specifications:

- **dependencies.md:** Detailed uv usage, dependency groups, cheat sheet
- **project_structure.md:** Architecture decisions and component responsibilities
- **feature_spec_stage1.md:** MVP feature specifications (current focus)
- **feature_spec_stage2.md:** Advanced features (WiFi, firewall, diagnostics)
- **feature_spec_stage3.md:** Professional tools (traffic analysis, VPN, VLANs)

**Read these documents when:**

- Implementing new features
- Understanding design rationale
- Planning large changes

## Trusting These Instructions

This documentation was generated through comprehensive exploration and testing of the repository. All commands have been validated to work correctly. Only search for additional information if:

- You encounter an error not covered here
- The instructions appear outdated (check file timestamps)
- You're implementing a feature not yet specified in the design docs

**When in doubt:**

1. Check `design/dependencies.md` for uv command details
1. Check `design/project_structure.md` for architecture questions
1. Run `uv run pytest -v` to verify your changes work
1. Run `uv run --group lint pre-commit run --all-files` before committing
