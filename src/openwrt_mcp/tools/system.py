"""System tools."""

from typing import Dict, Any
from fastmcp import FastMCP
from openwrt_mcp.managers import DeviceManager, ConnectionManager


def register_system_tools(
    mcp: FastMCP, device_manager: DeviceManager, connection_manager: ConnectionManager
):
    """Register system tools."""

    @mcp.tool()
    async def get_system_info(device_name: str) -> Dict[str, Any]:
        """Get system information (board and info) from a device."""
        try:
            device = device_manager.get_device(device_name)
            client = await connection_manager.get_ubus_client(device)

            board = await client.call("system", "board")
            info = await client.call("system", "info")

            return {"board": board, "info": info}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool()
    async def reboot_device(device_name: str) -> str:
        """Reboot the device."""
        try:
            device = device_manager.get_device(device_name)
            client = await connection_manager.get_ubus_client(device)

            # system reboot usually doesn't return
            await client.call("system", "reboot")
            return f"Device '{device_name}' is rebooting."
        except Exception as e:
            return f"Error rebooting device: {e}"
