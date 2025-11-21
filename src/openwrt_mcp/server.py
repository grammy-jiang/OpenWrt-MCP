"""OpenWrt MCP Server implementation."""

from fastmcp import FastMCP
from openwrt_mcp.db.engine import init_db, engine
from openwrt_mcp.managers import DeviceManager, ConnectionManager
from openwrt_mcp.tools import (
    register_registry_tools,
    register_system_tools,
    register_network_tools,
    register_uci_tools,
)

# Initialize Database
init_db()

# Initialize Managers
device_manager = DeviceManager(engine)
connection_manager = ConnectionManager()

# Initialize FastMCP server
mcp = FastMCP("OpenWrt MCP")

# Register Tools
register_registry_tools(mcp, device_manager)
register_system_tools(mcp, device_manager, connection_manager)
register_network_tools(mcp, device_manager, connection_manager)
register_uci_tools(mcp, device_manager, connection_manager)
