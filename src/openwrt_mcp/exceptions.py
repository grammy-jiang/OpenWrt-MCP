"""Custom exceptions for OpenWrt MCP Server."""


class OpenWrtMCPError(Exception):
    """Base exception for OpenWrt MCP."""

    pass


class DeviceNotFoundError(OpenWrtMCPError):
    """Raised when a device is not found in the registry."""

    pass


class DeviceConnectionError(OpenWrtMCPError):
    """Raised when connection to a device fails."""

    pass


class UbusError(OpenWrtMCPError):
    """Raised when a Ubus request fails."""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Ubus Error {code}: {message}")


class SSHError(OpenWrtMCPError):
    """Raised when an SSH command fails."""

    pass


class AuthenticationError(OpenWrtMCPError):
    """Raised when authentication fails."""

    pass
