# OpenWrt-MCP Feature Roadmap

This document categorizes features into three stages of implementation: Core Essentials (MVP), Advanced Management, and Professional/Niche.

## Stage 1: Core Essentials (MVP)

**Goal:** Establish connectivity, observability, and basic configuration. These are the "must-haves" to make the tool useful immediately.

| Feature                 | Description                                                                    | Underlying API (Likely)                             | API Type   |
| :---------------------- | :----------------------------------------------------------------------------- | :-------------------------------------------------- | :--------- |
| **Instance Management** | CRUD for Device Registry. Persist connection details (Host/Authentication).    | Internal JSON / Configuration                       | Local      |
| **System Health**       | Get model, firmware version, uptime, load average, memory usage.               | `system.board`, `system.info`                       | Ubus       |
| **Interface Status**    | List WAN/LAN status, IP addresses, uptime, RX/TX counters.                     | `network.interface.dump`                            | Ubus       |
| **Client List**         | List connected devices via DHCP leases and active WiFi associations.           | `dhcp.ipv4.leases`, `hostapd.get_clients`, `iwinfo` | Ubus       |
| **Basic UCI**           | Read config values, set simple values (e.g., SSID, passwords), commit changes. | `uci get`, `uci set`, `uci commit`                  | Ubus (UCI) |
| **Service Control**     | Restart key services (network, dnsmasq, firewall) and reboot the device.       | `service` list/call, `system` reboot                | Ubus       |

## Stage 2: Advanced Management

**Goal:** Enable day-to-day administration and troubleshooting. These features cover 80% of user needs.

| Feature             | Description                                                                 | Underlying API (Likely)       | API Type   |
| :------------------ | :-------------------------------------------------------------------------- | :---------------------------- | :--------- |
| **WiFi Survey**     | Scan for neighboring networks to find clear channels.                       | `iwinfo scan`                 | Ubus       |
| **Firewall Rules**  | Add/Remove Port Forwarding and Traffic Rules.                               | `uci` (firewall config)       | Ubus (UCI) |
| **Diagnostics**     | Run Ping, Traceroute, and NSLookup _from_ the router to debug connectivity. | `ping`, `traceroute` binaries | SSH / Exec |
| **Log Analysis**    | Read system and kernel logs (`logread`, `dmesg`) with keyword filtering.    | `logread`                     | SSH / Exec |
| **Access Control**  | Block/Allow specific MAC addresses (Parental Control basics).               | `hostapd` or firewall rules   | Ubus (UCI) |
| **Package Manager** | List, install, and update OpenWrt packages (`opkg`).                        | `opkg` CLI                    | SSH / Exec |

## Stage 3: Professional / Niche

**Goal:** Features for ISPs, fleet managers, or complex enterprise network setups.

| Feature              | Description                                                                  | Underlying API (Likely)        | API Type    |
| :------------------- | :--------------------------------------------------------------------------- | :----------------------------- | :---------- |
| **Traffic Analysis** | Real-time bandwidth usage per client or interface (requires extra packages). | `nlbwmon` or `conntrack`       | Ubus / File |
| **VPN Manager**      | Configure WireGuard or OpenVPN peers and tunnels.                            | `uci` (network/vpn), `wg` tool | Ubus (UCI)  |
| **VLAN/Switching**   | Complex VLAN tagging and bridge configuration (DSA).                         | `network` (DSA)                | Ubus (UCI)  |
| **Fleet Operations** | Automated Firmware Upgrades (`sysupgrade`) and Configuration Backup/Restore. | `sysupgrade`, `fs`             | SSH / Exec  |
| **Custom Scripts**   | Upload and execute arbitrary shell scripts (High security risk).             | SSH / `exec`                   | SSH / Exec  |
| **Mesh/Roaming**     | Configure 802.11r/s fast roaming and mesh parameters.                        | `uci` (wireless)               | Ubus (UCI)  |
