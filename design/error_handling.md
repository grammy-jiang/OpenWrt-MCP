<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Error Handling Strategy](#error-handling-strategy)
  - [1. Philosophy](#1-philosophy)
  - [2. Common Error Categories](#2-common-error-categories)
  - [3. Implementation Pattern](#3-implementation-pattern)
  - [4. Ubus Error Codes](#4-ubus-error-codes)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Error Handling Strategy

This document defines the standard error handling strategy for the OpenWrt-MCP server. The goal is to prevent server crashes and provide the AI (and user) with actionable error messages.

## 1. Philosophy

- **Never Crash:** The server should catch all exceptions raised during tool execution.
- **Informative:** Error messages should explain _what_ went wrong (Connection? Auth? Logic?) and _how_ to fix it.
- **Standardized:** Use a common set of exception classes or error formats.

## 2. Common Error Categories

| Error Type              | Description                                       | Example Message                                                           |
| :---------------------- | :------------------------------------------------ | :------------------------------------------------------------------------ |
| **ConnectionError**     | Unable to reach the OpenWrt device.               | "Could not connect to device 'main-router' at 192.168.1.1. Is it online?" |
| **AuthError**           | Invalid username or password.                     | "Authentication failed for user 'root'. Please check credentials."        |
| **DeviceNotFoundError** | The requested device name is not in the registry. | "Device 'living-room-ap' not found. Available devices: ['main-router']."  |
| **UbusError**           | The Ubus call returned an error code.             | "Ubus call 'system.board' failed: Code 4 (Not Found)."                    |
| **TimeoutError**        | The operation took too long.                      | "Request to '192.168.1.1' timed out after 10 seconds."                    |

## 3. Implementation Pattern

All tools should follow this pattern:

```python
def my_tool(device_name: str = None):
    try:
        device = device_manager.get_device(device_name)
        result = device.ubus_call(method, params)
        return result
    except DeviceNotFoundError:
        return "Error: Device not found. Please check the name."
    except AuthError:
        return "Error: Authentication failed. Please update credentials."
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"
```

## 4. Ubus Error Codes

When a Ubus call fails, it returns a numeric code. The MCP server should translate these into human-readable strings.

| Code | Meaning           |
| :--- | :---------------- |
| 0    | Success           |
| 1    | Invalid Command   |
| 2    | Invalid Argument  |
| 3    | Method Not Found  |
| 4    | Not Found         |
| 5    | No Data           |
| 6    | Permission Denied |
| 7    | Timeout           |
| 8    | Not Supported     |
