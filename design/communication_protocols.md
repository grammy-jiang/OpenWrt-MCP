<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [OpenWrt Communication Protocols](#openwrt-communication-protocols)
  - [Overview of Methods](#overview-of-methods)
    - [1. Ubus (OpenWrt Micro Bus Architecture)](#1-ubus-openwrt-micro-bus-architecture)
    - [2. SSH (Secure Shell)](#2-ssh-secure-shell)
    - [3. UCI (Unified Configuration Interface)](#3-uci-unified-configuration-interface)
    - [4. LuCI (Web Interface) RPC](#4-luci-web-interface-rpc)
  - [Comparison Table](#comparison-table)
  - [Pros and Cons](#pros-and-cons)
    - [Ubus (Recommended)](#ubus-recommended)
    - [SSH](#ssh)
    - [LuCI RPC](#luci-rpc)
  - [Connectivity & API Strategy](#connectivity--api-strategy)
    - [A. Primary (Implement First)](#a-primary-implement-first)
    - [B. Secondary (Add Later)](#b-secondary-add-later)
    - [C. Optional/Edge](#c-optionaledge)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# OpenWrt Communication Protocols

This document explores the various APIs and methods available for communicating with and controlling an OpenWrt device programmatically, specifically for the design of the OpenWrt MCP server.

## Overview of Methods

### 1. Ubus (OpenWrt Micro Bus Architecture)

**The Native IPC.**
Ubus is the core Inter-Process Communication mechanism in OpenWrt. It allows system daemons (like `netifd`, `procd`) to expose methods and listen for events.

- **Access:**
  - **Local:** `ubus` CLI or C/Lua libraries.
  - **Remote:** JSON-RPC over HTTP via `uhttpd-mod-ubus`.
- **Best For:** Programmatic control, state retrieval, and configuration management.

### 2. SSH (Secure Shell)

**The Sysadmin Standard.**
Standard shell access using Dropbear.

- **Access:** TCP Port 22.
- **Best For:** Initial setup, debugging, "break-glass" scenarios, and complex file operations.

### 3. UCI (Unified Configuration Interface)

**The Configuration Manager.**
Not a transport protocol, but the centralized configuration system.

- **Access:** Via SSH (`uci set`) or Ubus (`ubus call uci`).
- **Best For:** Persistent configuration changes.

### 4. LuCI (Web Interface) RPC

**The Web Backend.**
The RPC interface used by the LuCI web UI.

- **Access:** HTTP at `/cgi-bin/luci/rpc/`.
- **Best For:** High-level logic that aggregates multiple low-level calls (though often heavier).

---

## Comparison Table

| Feature          | Ubus (JSON-RPC)                 | SSH (Shell)               | LuCI RPC                 |
| :--------------- | :------------------------------ | :------------------------ | :----------------------- |
| **Transport**    | HTTP / Unix Socket              | TCP (Port 22)             | HTTP                     |
| **Data Format**  | **JSON (Structured)**           | Text (Unstructured)       | JSON                     |
| **Performance**  | **High** (C-based, lightweight) | Low (Connection overhead) | Medium (Lua interpreter) |
| **Granularity**  | **High** (Fine-grained ACLs)    | Low (All-or-nothing Root) | Medium                   |
| **State Access** | Real-time (via daemons)         | Parsed from commands      | Real-time                |
| **Reliability**  | High (API contract)             | Low (Screen scraping)     | Medium                   |

## Pros and Cons

### Ubus (Recommended)

| Pros                                                            | Cons                                                                    |
| :-------------------------------------------------------------- | :---------------------------------------------------------------------- |
| **Structured Data:** Returns clean JSON, perfect for MCP tools. | **Documentation:** Can be sparse; requires exploration via `ubus list`. |
| **Native:** Lowest overhead, direct access to system daemons.   | **Setup:** Requires `uhttpd-mod-ubus` (usually present) and ACL config. |
| **Security:** Supports granular Access Control Lists (ACLs).    |                                                                         |

### SSH

| Pros                                                         | Cons                                                            |
| :----------------------------------------------------------- | :-------------------------------------------------------------- |
| **Ubiquitous:** Available on virtually every OpenWrt device. | **Unstructured:** Requires parsing text output (fragile).       |
| **Power:** Can do absolutely anything (root access).         | **Slow:** Connection handshake is expensive for frequent calls. |
| **Zero-Config:** Works out of the box.                       | **Security:** Hard to restrict specific actions.                |

### LuCI RPC

| Pros                                               | Cons                                                            |
| :------------------------------------------------- | :-------------------------------------------------------------- |
| **High-Level:** Abstractions for complex tasks.    | **Heavy:** Often spawns Lua interpreters.                       |
| **Feature Rich:** Mirrors the web UI capabilities. | **Future:** Moving towards client-side rendering (Ubus-direct). |

## Connectivity & API Strategy

### A. Primary (Implement First)

1. **ubus (Local + HTTP JSON-RPC via `rpcd`/`uhttpd`)**

   - **Role:** Native, structured, fast communication.
   - **Usage:** Map MCP tools 1:1 to ubus methods (e.g., `uci`, `network.device`, `system`, `hostapd`, `iwinfo`).

1. **UCI via ubus (`uci` object)**

   - **Role:** Configuration management.
   - **Usage:** Treat UCI as the single source of truth. Use `ubus call uci <args>` for all config changes to avoid shell parsing. Read-only file reads can be used where necessary.

1. **SSH (`dropbear`/`OpenSSH`) with Strict Whitelist**

   - **Role:** Fallback mechanism.
   - **Usage:** Only used when ubus coverage is missing. Execution is limited to curated binaries (e.g., `fw4`, `logread`, specific `ubus call` wrappers) to ensure safety.

### B. Secondary (Add Later)

1. **`rpcd` Custom Plugins**

   - **Goal:** Add missing capabilities not exposed by default.
   - **Usage:** Implement atomic batched changes or zero-touch playbooks.

1. **Procd Hooks & Service Control**

   - **Goal:** Standardize service management.
   - **Usage:** Unified start/stop/reload/status commands with structured responses.

1. **ubus Events Subscription**

   - **Goal:** Real-time monitoring.
   - **Usage:** Stream health, client association, and state changes (from `hostapd`, `netifd`).

### C. Optional/Edge

1. **LuCI JSON-RPC**

   - Only considered for legacy environments where `rpcd` extensions are missing.

1. **NetJSON Export**

   - For potential integration with external control planes or Network Management Systems (NMS).
