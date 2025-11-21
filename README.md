<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [OpenWrt-MCP](#openwrt-mcp)
  - [Features Summary](#features-summary)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# OpenWrt-MCP

`OpenWrt-MCP` is a production-minded MCP server for OpenWrt built with
Python/FastMCP. It exposes guardrailed tools for UCI/ubus operations,
service control (dnsmasq, firewall4, hostapd), system facts, and
health/telemetry collection. The goal is simple: reproducible,
auditable network operations—whether you run one router or a fleet.

## Features Summary

| Feature                 | Description                                             | Phase         | Status     |
| :---------------------- | :------------------------------------------------------ | :------------ | :--------- |
| **Instance Management** | Manage device registry (add, remove, list devices).     | Stage 1 (MVP) | ❌ Planned |
| **System Health**       | Retrieve system board and info (model, uptime, memory). | Stage 1 (MVP) | ❌ Planned |
| **Interface Status**    | Dump network interface status.                          | Stage 1 (MVP) | ❌ Planned |
| **Basic UCI**           | Get, set, and commit UCI configurations.                | Stage 1 (MVP) | ❌ Planned |
| **Service Control**     | Reboot device. (Service restart pending).               | Stage 1 (MVP) | ❌ Planned |
| **Client List**         | List connected DHCP/WiFi clients.                       | Stage 1 (MVP) | ❌ Planned |
| **Advanced Management** | WiFi survey, firewall rules, diagnostics, logs.         | Stage 2       | ❌ Planned |
| **Professional Tools**  | Traffic analysis, VPN, VLANs, fleet ops.                | Stage 3       | ❌ Planned |

For development instructions, please refer to [design/dependencies.md](design/dependencies.md).
