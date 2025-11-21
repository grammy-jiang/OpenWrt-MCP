<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Project Structure](#project-structure)
  - [1. Directory Layout](#1-directory-layout)
  - [2. Component Responsibilities](#2-component-responsibilities)
    - [`src/openwrt_mcp/main.py`](#srcopenwrt_mcpmainpy)
    - [`src/openwrt_mcp/db/`](#srcopenwrt_mcpdb)
    - [`src/openwrt_mcp/managers/`](#srcopenwrt_mcpmanagers)
    - [`src/openwrt_mcp/utils/`](#srcopenwrt_mcputils)
    - [`src/openwrt_mcp/tools/`](#srcopenwrt_mcptools)
  - [3. Packaging Strategy](#3-packaging-strategy)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Project Structure

This document outlines the architectural structure of the OpenWrt-MCP project, designed for packaging with `uv` and publishing to PyPI. It is structured to support the immediate Phase 1 implementation while providing specific extension points for Phase 2 and 3.

## 1. Directory Layout

We follow the `src`-layout, which is a best practice for modern Python packaging.

```text
openwrt-mcp/
├── pyproject.toml          # Project metadata and dependencies (managed by uv)
├── uv.lock                 # Dependency lockfile
├── .pre-commit-config.yaml # Code quality hooks configuration
├── README.md               # Project documentation
├── .env                    # Local secrets (gitignored)
├── src/
│   └── openwrt_mcp/        # Main package directory
│       ├── __init__.py     # Package marker
│       ├── main.py         # Entry point, FastMCP server definition
│       ├── config.py       # Configuration (Env vars, DB paths)
│       ├── exceptions.py   # Custom Exceptions (UbusError, DeviceNotFoundError)
│       ├── db/             # Database Layer
│       │   ├── __init__.py
│       │   ├── engine.py   # SQLModel engine setup & session management
│       │   └── models.py   # Database Entities (Device)
│       ├── managers/       # Business Logic & State Management
│       │   ├── __init__.py
│       │   ├── device_manager.py     # Registry Logic (CRUD)
│       │   └── connection_manager.py # Async HTTP/SSH session pooling
│       ├── tools/          # MCP Tool Definitions (The "Interface Layer")
│       │   ├── __init__.py
│       │   ├── registry.py # Stage 1: Instance Management
│       │   ├── system.py   # Stage 1: System Health & Services
│       │   ├── network.py  # Stage 1: Interfaces & Clients
│       │   ├── uci.py      # Stage 1: UCI Configuration
│       │   ├── _wifi.py    # Stage 2: WiFi Management (Future)
│       │   └── _traffic.py # Stage 3: Traffic Analysis (Future)
│       └── utils/          # Low-level Protocol & Parsing Utilities
│           ├── __init__.py
│           ├── ubus.py     # Async Ubus JSON-RPC client wrapper
│           ├── ssh.py      # Async SSH command wrapper (for Phase 2/3)
│           └── parsers.py  # Output parsers (for CLI tools like iwinfo, ping)
└── tests/                  # Test suite
    ├── __init__.py
    ├── conftest.py         # Pytest fixtures (asyncio setup, mock DB)
    ├── integration/        # End-to-end tests against mock Ubus
    └── unit/               # Unit tests for managers/utils
```

## 2. Component Responsibilities

### `src/openwrt_mcp/main.py`

- **Responsibility**: Application Entry Point.
- **Logic**:
  - Initializes the `FastMCP` application.
  - Loads configuration via `config.py`.
  - Registers tools from `src/openwrt_mcp/tools/`.
  - Starts the server.

### `src/openwrt_mcp/db/`

- **Responsibility**: Data Persistence.
- **`engine.py`**: Handles SQLite connection and `SQLModel` metadata creation.
- **`models.py`**: Defines the `Device` schema. Separating this allows easy addition of future models (e.g., `LogFilters` in Phase 2).

### `src/openwrt_mcp/managers/`

- **Responsibility**: Core Business Logic (The "Brain").
- **`device_manager.py`**: High-level API for the Device Registry. Decouples the MCP tools from the raw DB queries.
- **`connection_manager.py`**:
  - Manages `httpx.AsyncClient` for Ubus (primary).
  - Manages `asyncssh` connections (fallback).
  - **Extensibility**: Centralizes auth logic so we can add token rotation or different auth schemes later without touching tool code.

### `src/openwrt_mcp/utils/`

- **Responsibility**: Protocol Adapters (The "Hands").
- **`ubus.py`**:
  - Translates Python dicts to Ubus JSON-RPC.
  - Maps Ubus error codes to `exceptions.py`.
- **`ssh.py`**:
  - **Phase 2/3 Prep**: Will handle executing raw shell commands when Ubus isn't enough (e.g., `sysupgrade`, `ping`).
- **`parsers.py`**:
  - **Phase 2/3 Prep**: Will contain regex/logic to parse stdout from CLI tools into structured JSON.

### `src/openwrt_mcp/tools/`

- **Responsibility**: MCP Interface (The "Face").
- **Logic**:
  - Purely declarative.
  - Validates inputs using Pydantic (via FastMCP).
  - Calls `managers` to do the work.
  - Returns human-readable strings or structured JSON.
  - **Organization**: Grouped by domain (System, Network, UCI) to keep files small and maintainable.

## 3. Packaging Strategy

- **Build System**: `hatchling` or `setuptools` (via `uv build`).
- **Entry Point**: Defined in `pyproject.toml` so users can run `openwrt-mcp` directly.

  ```toml
  [project.scripts]
  openwrt-mcp = "openwrt_mcp.main:main"
  ```
