<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Feature Specification: Stage 2 (Advanced Management)](#feature-specification-stage-2-advanced-management)
  - [1. WiFi Survey](#1-wifi-survey)
    - [Tools](#tools)
  - [2. Firewall Rules](#2-firewall-rules)
    - [Tools](#tools-1)
  - [3. Diagnostics](#3-diagnostics)
    - [Tools](#tools-2)
  - [4. Log Analysis](#4-log-analysis)
    - [Tools](#tools-3)
  - [5. Access Control](#5-access-control)
    - [Tools](#tools-4)
  - [6. Package Manager](#6-package-manager)
    - [Tools](#tools-5)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Feature Specification: Stage 2 (Advanced Management)

This document details the technical specifications for "Advanced Management" features. These features enable day-to-day administration and troubleshooting.

## 1. WiFi Survey

**Goal:** Scan for neighboring networks to optimize channel selection.

### Tools

| Tool Name   | Arguments           | Implementation Details                                                                                            | API Called           |
| :---------- | :------------------ | :---------------------------------------------------------------------------------------------------------------- | :------------------- |
| `wifi_scan` | `device_name` (opt) | **Calls:** `iwinfo wlan0 scan` (via ubus or exec).<br>**Returns:** List of `{ssid, channel, signal, encryption}`. | `iwinfo` (ubus/exec) |

## 2. Firewall Rules

**Goal:** Manage port forwarding and traffic rules.

### Tools

| Tool Name             | Arguments                                                                 | Implementation Details                                                      | API Called       |
| :-------------------- | :------------------------------------------------------------------------ | :-------------------------------------------------------------------------- | :--------------- |
| `add_port_forward`    | `name`, `proto`, `src_dport`, `dest_ip`, `dest_port`, `device_name` (opt) | **Calls:** `uci add firewall redirect`, `uci set …`, `uci commit firewall`. | `uci` (firewall) |
| `list_firewall_rules` | `device_name` (opt)                                                       | **Calls:** `uci get firewall`.                                              | `uci` (firewall) |

## 3. Diagnostics

**Goal:** Debug network connectivity from the router's perspective.

### Tools

| Tool Name    | Arguments                                         | Implementation Details                                                                              | API Called          |
| :----------- | :------------------------------------------------ | :-------------------------------------------------------------------------------------------------- | :------------------ |
| `ping_host`  | `target`, `count` (def: 3), `device_name` (opt)   | **Calls:** `ping -c <count> <target>` via SSH/Exec.<br>**Returns:** Success/Fail and latency stats. | `ping` (exec)       |
| `traceroute` | `target`, `device_name` (opt)                     | **Calls:** `traceroute <target>` via SSH/Exec.                                                      | `traceroute` (exec) |
| `nslookup`   | `domain`, `dns_server` (opt), `device_name` (opt) | **Calls:** `nslookup <domain>` via SSH/Exec.                                                        | `nslookup` (exec)   |

## 4. Log Analysis

**Goal:** Inspect system logs for errors or events.

### Tools

| Tool Name          | Arguments                                              | Implementation Details                                                 | API Called       |
| :----------------- | :----------------------------------------------------- | :--------------------------------------------------------------------- | :--------------- |
| `read_logs`        | `lines` (def: 50), `filter` (opt), `device_name` (opt) | **Calls:** `logread \| tail -n <lines>` or `logread \| grep <filter>`. | `logread` (exec) |
| `read_kernel_logs` | `lines` (def: 50), `device_name` (opt)                 | **Calls:** `dmesg \| tail -n <lines>`.                                 | `dmesg` (exec)   |

## 5. Access Control

**Goal:** Block or allow specific devices.

### Tools

| Tool Name     | Arguments                          | Implementation Details                                                                                                                                                                      | API Called       |
| :------------ | :--------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------- |
| `block_mac`   | `mac_address`, `device_name` (opt) | **Strategy:** Add firewall traffic rule to drop input from MAC.<br>**Calls:** `uci add firewall rule`, `src=*`, `src_mac=<mac>`, `target=DROP`.<br>**Returns:** String "MAC <mac> blocked." | `uci` (firewall) |
| `unblock_mac` | `mac_address`, `device_name` (opt) | **Strategy:** Find and remove firewall rule with `src_mac=<mac>`.<br>**Returns:** String "MAC <mac> unblocked."                                                                             | `uci` (firewall) |

## 6. Package Manager

**Goal:** Install and update software.

### Tools

| Tool Name         | Arguments                            | Implementation Details                           | API Called    |
| :---------------- | :----------------------------------- | :----------------------------------------------- | :------------ |
| `list_packages`   | `pattern` (opt), `device_name` (opt) | **Calls:** `opkg list-installed`.                | `opkg` (exec) |
| `install_package` | `package_name`, `device_name` (opt)  | **Calls:** `opkg update && opkg install <name>`. | `opkg` (exec) |
