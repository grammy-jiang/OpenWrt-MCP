"""Tools package."""

from openwrt_mcp.tools.registry import register_registry_tools
from openwrt_mcp.tools.system import register_system_tools
from openwrt_mcp.tools.network import register_network_tools
from openwrt_mcp.tools.uci import register_uci_tools

__all__ = [
    "register_registry_tools",
    "register_system_tools",
    "register_network_tools",
    "register_uci_tools",
]
