"""Registry tools."""

from typing import List
from fastmcp import FastMCP
from openwrt_mcp.managers import DeviceManager


def register_registry_tools(mcp: FastMCP, device_manager: DeviceManager):
    """Register device registry tools."""

    @mcp.tool()
    async def list_devices() -> List[str]:
        """List all registered OpenWrt devices."""
        devices = device_manager.list_devices()
        return [d.name for d in devices]

    @mcp.tool()
    async def add_device(
        name: str,
        host: str,
        username: str,
        password: str,
        port: int = 22,
        use_ssl: bool = False,
        description: str | None = None,
    ) -> str:
        """Add a new OpenWrt device to the registry."""
        try:
            device_manager.create_device(
                name=name,
                host=host,
                username=username,
                password=password,
                port=port,
                use_ssl=use_ssl,
                description=description,
            )
            return f"Device '{name}' added successfully."
        except Exception as e:
            return f"Error adding device: {e}"

    @mcp.tool()
    async def remove_device(name: str) -> str:
        """Remove a device from the registry."""
        try:
            device_manager.delete_device(name)
            return f"Device '{name}' removed successfully."
        except Exception as e:
            return f"Error removing device: {e}"
