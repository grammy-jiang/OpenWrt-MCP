<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Feature Specification: Stage 3 (Professional / Niche)](#feature-specification-stage-3-professional--niche)
  - [1. Traffic Analysis](#1-traffic-analysis)
    - [Tools](#tools)
  - [2. VPN Manager](#2-vpn-manager)
    - [Tools](#tools-1)
  - [3. VLAN/Switching](#3-vlanswitching)
    - [Tools](#tools-2)
    - [Tools](#tools-3)
  - [4. Fleet Operations](#4-fleet-operations)
    - [Tools](#tools-4)
  - [5. Custom Scripts](#5-custom-scripts)
    - [Tools](#tools-5)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Feature Specification: Stage 3 (Professional / Niche)

This document details the technical specifications for "Professional" features, targeting ISPs, fleet managers, and complex enterprise setups.

## 1. Traffic Analysis

**Goal:** Monitor real-time bandwidth usage per client.

### Tools

| Tool Name           | Arguments                              | Implementation Details                                                                                                      | API Called              |
| :------------------ | :------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------- | :---------------------- |
| `get_traffic_stats` | `interface` (opt), `device_name` (opt) | **Calls:** `nlbwmon` (if installed) or parse `/proc/net/dev` or `conntrack` table.<br>**Returns:** Bytes in/out per IP/MAC. | `nlbwmon` / `conntrack` |

## 2. VPN Manager

**Goal:** Configure WireGuard or OpenVPN.

### Tools

| Tool Name            | Arguments                                        | Implementation Details                                           | API Called      |
| :------------------- | :----------------------------------------------- | :--------------------------------------------------------------- | :-------------- |
| `add_wireguard_peer` | `public_key`, `allowed_ips`, `device_name` (opt) | **Calls:** UCI commands to `network` config (proto `wireguard`). | `uci` (network) |
| `get_vpn_status`     | `device_name` (opt)                              | **Calls:** `wg show` via SSH/Exec.                               | `wg` (exec)     |

## 3. VLAN/Switching

**Goal:** Configure complex network segmentation.

### Tools

### Tools

| Tool Name        | Arguments                                                    | Implementation Details                                                                 | API Called      |
| :--------------- | :----------------------------------------------------------- | :------------------------------------------------------------------------------------- | :-------------- |
| `configure_vlan` | `interface`, `vlan_id`, `tagged` (bool), `device_name` (opt) | **Calls:** UCI commands for DSA (Distributed Switch Architecture) in `network` config. | `uci` (network) |

## 4. Fleet Operations

**Goal:** Manage multiple devices at scale.

### Tools

| Tool Name          | Arguments                          | Implementation Details                                                                                              | API Called          |
| :----------------- | :--------------------------------- | :------------------------------------------------------------------------------------------------------------------ | :------------------ |
| `backup_config`    | `device_name` (opt)                | **Calls:** `sysupgrade -b /tmp/backup.tar.gz` and download file via SCP/HTTP.                                       | `sysupgrade` (exec) |
| `restore_config`   | `backup_file`, `device_name` (opt) | **Calls:** Upload file and run `sysupgrade -r`.                                                                     | `sysupgrade` (exec) |
| `upgrade_firmware` | `image_url`, `device_name` (opt)   | **Calls:** `sysupgrade -v <url>`. **High Risk.**<br>**Returns:** String "Upgrade started. Connection will be lost." | `sysupgrade` (exec) |

## 5. Custom Scripts

**Goal:** Execute arbitrary logic.

### Tools

| Tool Name    | Arguments                             | Implementation Details                                                         | API Called   |
| :----------- | :------------------------------------ | :----------------------------------------------------------------------------- | :----------- |
| `run_script` | `script_content`, `device_name` (opt) | **Calls:** Write content to `/tmp/script.sh`, `chmod +x`, and execute via SSH. | `exec` (ssh) |
