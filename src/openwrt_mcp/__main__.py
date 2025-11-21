"""Entry point for the OpenWrt MCP Server."""

import argparse
from openwrt_mcp.server import mcp
from openwrt_mcp import __version__


def main():
    """Run the MCP server."""
    parser = argparse.ArgumentParser(description="OpenWrt MCP Server")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport mode (default: stdio)",
    )
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host for SSE (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port for SSE (default: 8000)"
    )

    args = parser.parse_args()

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
