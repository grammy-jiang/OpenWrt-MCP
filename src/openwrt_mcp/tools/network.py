"""Network tools."""

from typing import Dict, Any
from fastmcp import FastMCP
from openwrt_mcp.managers import DeviceManager, ConnectionManager


def register_network_tools(
    mcp: FastMCP, device_manager: DeviceManager, connection_manager: ConnectionManager
):
    """Register network tools."""

    @mcp.tool()
    async def get_interfaces(device_name: str) -> Dict[str, Any]:
        """Get network interfaces status."""
        try:
            device = device_manager.get_device(device_name)
            client = await connection_manager.get_ubus_client(device)

            # network.interface dump
            result = await client.call("network.interface", "dump")
            return result
        except Exception as e:
            return {"error": str(e)}
