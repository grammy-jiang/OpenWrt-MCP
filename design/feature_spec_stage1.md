<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Feature Specification: Stage 1 (Core Essentials)](#feature-specification-stage-1-core-essentials)
  - [1. Instance Management (Device Registry)](#1-instance-management-device-registry)
    - [Data Storage](#data-storage)
    - [Tools](#tools)
  - [2. System Health](#2-system-health)
    - [Tools](#tools-1)
  - [3. Interface Status](#3-interface-status)
    - [Tools](#tools-2)
  - [4. Client List](#4-client-list)
    - [Tools](#tools-3)
  - [5. Basic UCI (Configuration)](#5-basic-uci-configuration)
    - [Tools](#tools-4)
  - [6. Service Control](#6-service-control)
    - [Tools](#tools-5)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Feature Specification: Stage 1 (Core Essentials)

This document details the technical specifications for the "Core Essentials" features. These are the foundational blocks required to establish connectivity, observability, and basic configuration.

## 1. Instance Management (Device Registry)

**Goal:** Allow the AI to dynamically add, remove, and switch between different OpenWrt devices (e.g., "Main Router", "Living Room AP") without restarting the server.

### Data Storage

- **Database:** SQLite (`~/.config/openwrt-mcp/devices.db`)
- **ORM:** SQLModel or SQLAlchemy
- **Model:** `Device`
  - `name` (str, Primary Key)
  - `host` (str)
  - `username` (str, Default 'root')
  - `password` (str)
  - `protocol` (str, Default 'http')
  - `port` (int, Default 80)

### Tools

| Tool Name       | Arguments                                                      | Implementation Details                                                                                                                               | API Called                  |
| :-------------- | :------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------- |
| `add_device`    | `name` (req), `host` (req), `username`, `password`, `protocol` | **Action:** Validate connectivity (ping/ubus). Create `Device` object and save via ORM.<br>**Returns:** String "Device '<name>' added successfully." | `system.board` (validation) |
| `remove_device` | `name` (req)                                                   | **Action:** Delete `Device` object via ORM.<br>**Returns:** String "Device '<name>' removed."                                                        | Internal                    |
| `list_devices`  | None                                                           | **Action:** Query all `Device` objects.<br>**Returns:** List of `{name, host, status}` (mask passwords).                                             | Internal                    |
| `update_device` | `name` (req), `host`, `password`, …                          | **Action:** Fetch `Device`, update fields, save via ORM.<br>**Returns:** String "Device '<name>' updated."                                           | Internal                    |

---

## 2. System Health

**Goal:** Provide high-level device status.

### Tools

| Tool Name         | Arguments           | Implementation Details                                                                                 | API Called             |
| :---------------- | :------------------ | :----------------------------------------------------------------------------------------------------- | :--------------------- |
| `get_system_info` | `device_name` (opt) | **Calls:** `system board` via ubus.<br>**Returns:** JSON `{hostname, model, system, release, kernel}`. | `system board` (ubus)  |
| `reboot_device`   | `device_name` (opt) | **Calls:** `system reboot` via ubus.<br>**Returns:** String "Reboot initiated."                        | `system reboot` (ubus) |

---

## 3. Interface Status

**Goal:** Monitor network connectivity.

### Tools

| Tool Name        | Arguments           | Implementation Details                                                                                                        | API Called               |
| :--------------- | :------------------ | :---------------------------------------------------------------------------------------------------------------------------- | :----------------------- |
| `get_interfaces` | `device_name` (opt) | **Calls:** `ubus call network.interface dump`<br>**Returns:** List of `{interface: "wan", ip: "…", up: true, uptime: 123}`. | `network.interface.dump` |

---

## 4. Client List

**Goal:** Identify what is connected to the network.

### Tools

| Tool Name               | Arguments           | Implementation Details                                                                                                                                                                                                                                             | API Called                                |
| :---------------------- | :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------- |
| `get_connected_clients` | `device_name` (opt) | **Strategy:** Combine DHCP and WiFi data.<br>1. **DHCP:** `ubus call dhcp ipv4_leases`.<br>2. **WiFi:** `ubus call hostapd.wlan0 get_clients`.<br>3. **Merge:** Join on MAC.<br>**Returns:** List of `{mac, ip, hostname, signal, interface, type: "wifi/wired"}`. | `dhcp.ipv4_leases`, `hostapd.get_clients` |

---

## 5. Basic UCI (Configuration)

**Goal:** Read and write configuration.

### Tools

| Tool Name     | Arguments                                                   | Implementation Details                                                                 | API Called    |
| :------------ | :---------------------------------------------------------- | :------------------------------------------------------------------------------------- | :------------ |
| `uci_get`     | `config`, `section`, `option` (opt), `device_name` (opt)    | **Calls:** `ubus call uci get …`<br>**Returns:** String value or JSON object.          | `uci.get`     |
| `uci_set`     | `config`, `section`, `option`, `value`, `device_name` (opt) | **Calls:** `ubus call uci set …`<br>**Returns:** String "Set successful".              | `uci.set`     |
| `uci_commit`  | `config`, `device_name` (opt)                               | **Calls:** `ubus call uci commit …`<br>**Returns:** String "Commit successful".        | `uci.commit`  |
| `uci_changes` | `config`, `device_name` (opt)                               | **Calls:** `ubus call uci changes …`<br>**Returns:** JSON object of pending changes.   | `uci.changes` |

---

## 6. Service Control

**Goal:** Manage system services.

### Tools

| Tool Name         | Arguments                           | Implementation Details                                                                                                          | API Called                              |
| :---------------- | :---------------------------------- | :------------------------------------------------------------------------------------------------------------------------------ | :-------------------------------------- |
| `restart_service` | `service_name`, `device_name` (opt) | **Primary:** `service <name> restart` (via SSH) or `ubus call service …`.<br>**Returns:** String "Service restart initiated." | `service.list`, `service.call` (or SSH) |
