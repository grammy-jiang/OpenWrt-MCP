<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [OpenWrt MCP Server - Design Summary](#openwrt-mcp-server---design-summary)
  - [Architecture & Roadmap](#architecture--roadmap)
  - [Detailed Feature Specifications](#detailed-feature-specifications)
  - [Next Steps](#next-steps)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# OpenWrt MCP Server - Design Summary

This directory contains the complete design specifications for the OpenWrt MCP Server.

## Architecture & Roadmap

- **[Project Structure](project_structure.md)**: Outlines the Python package layout, component responsibilities, and database choice (SQLite + SQLModel).
- **[Feature Roadmap](feature_roadmap.md)**: High-level plan divided into 3 stages (Essentials, Advanced, Professional).
- **[Communication Protocols](communication_protocols.md)**: Analysis of Ubus vs. SSH vs. LuCI, selecting Ubus as the primary transport.
- **[Dependencies & Environment](dependencies.md)**: Selection of `uv`, `fastmcp`, `sqlmodel`, `httpx`, and `asyncssh`.
- **[Error Handling](error_handling.md)**: Strategy for mapping Ubus error codes to user-friendly messages.

## Detailed Feature Specifications

These documents contain the "implementation-ready" specs, including tool names, arguments, specific API calls, and return values.

- **[Stage 1: Core Essentials](feature_spec_stage1.md)**

  - Instance Management (Device Registry)
  - System Health
  - Interface Status
  - Client List
  - Basic UCI Configuration
  - Service Control

- **[Stage 2: Advanced Network & Logs](feature_spec_stage2.md)**

  - WiFi Management
  - Firewall Management
  - Diagnostic Tools (Ping, Traceroute)
  - Log Retrieval

- **[Stage 3: Professional Traffic & VPN](feature_spec_stage3.md)**
  - Traffic Monitoring
  - VPN Management (WireGuard/OpenVPN)
  - System Maintenance (Backup/Upgrade)
  - Custom Scripts

## Next Steps

The design phase is complete. The next phase is **Implementation of Stage 1**.
