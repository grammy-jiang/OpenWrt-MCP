"""Connection manager."""

from typing import Dict
from openwrt_mcp.utils.ubus import UbusClient
from openwrt_mcp.utils.ssh import SSHClient
from openwrt_mcp.db.models import Device


class ConnectionManager:
    """Manager for device connections."""

    def __init__(self):
        self._ubus_clients: Dict[str, UbusClient] = {}
        self._ssh_clients: Dict[str, SSHClient] = {}

    async def get_ubus_client(self, device: Device) -> UbusClient:
        """Get a Ubus client for a device."""
        if device.name in self._ubus_clients:
            # Check if connected? UbusClient doesn't have is_connected check easily without request.
            # For now, return existing. If it fails, we might need to reconnect.
            return self._ubus_clients[device.name]

        client = UbusClient(
            base_url=f"{'https' if device.use_ssl else 'http'}://{device.host}",
            username=device.username,
            password=device.password,
            verify_ssl=False,  # For now, ignore SSL verification for self-signed certs common on routers
        )
        # We need to initialize it (login)
        await client.login()
        self._ubus_clients[device.name] = client
        return client

    async def get_ssh_client(self, device: Device) -> SSHClient:
        """Get an SSH client for a device."""
        if device.name in self._ssh_clients:
            return self._ssh_clients[device.name]

        client = SSHClient(
            host=device.host,
            username=device.username,
            password=device.password,
            port=device.port,
        )
        await client.connect()
        self._ssh_clients[device.name] = client
        return client

    async def close_all(self):
        """Close all connections."""
        for client in self._ubus_clients.values():
            # UbusClient needs a close method or we access _client directly
            if client._client:
                await client._client.aclose()
        self._ubus_clients.clear()

        for client in self._ssh_clients.values():
            # SSHClient needs a close method
            if client._conn:
                client._conn.close()
                await client._conn.wait_closed()
        self._ssh_clients.clear()
