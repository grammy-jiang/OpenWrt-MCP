"""UCI tools."""

from typing import Dict, Any, Optional, Union
from fastmcp import FastMCP
from openwrt_mcp.managers import DeviceManager, ConnectionManager


def register_uci_tools(
    mcp: FastMCP, device_manager: DeviceManager, connection_manager: ConnectionManager
):
    """Register UCI tools."""

    @mcp.tool()
    async def uci_get(
        device_name: str, config: str, section: str, option: Optional[str] = None
    ) -> Union[str, Dict[str, Any]]:
        """Get UCI configuration value."""
        try:
            device = device_manager.get_device(device_name)
            client = await connection_manager.get_ubus_client(device)

            args = {"config": config, "section": section}
            if option:
                args["option"] = option

            result = await client.call("uci", "get", args)
            # Result format depends on ubus uci implementation.
            # Usually {"value": ...}
            return result
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    async def uci_set(
        device_name: str, config: str, section: str, values: Dict[str, Any]
    ) -> str:
        """Set UCI configuration values."""
        try:
            device = device_manager.get_device(device_name)
            client = await connection_manager.get_ubus_client(device)

            args = {"config": config, "section": section, "values": values}
            await client.call("uci", "set", args)
            return "Successfully set values."
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    async def uci_commit(device_name: str, config: str) -> str:
        """Commit UCI configuration."""
        try:
            device = device_manager.get_device(device_name)
            client = await connection_manager.get_ubus_client(device)

            await client.call("uci", "commit", {"config": config})
            return f"Successfully committed {config}."
        except Exception as e:
            return f"Error: {e}"
