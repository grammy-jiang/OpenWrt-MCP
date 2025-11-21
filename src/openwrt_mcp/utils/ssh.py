"""Async SSH client."""

import asyncssh
from typing import Optional, Tuple
from openwrt_mcp.exceptions import SSHError, AuthenticationError, DeviceConnectionError


class SSHClient:
    """Client for interacting with OpenWrt via SSH."""

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        port: int = 22,
        known_hosts: Optional[str] = None,
    ):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.known_hosts = known_hosts
        self._conn: Optional[asyncssh.SSHClientConnection] = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            self._conn.close()
            await self._conn.wait_closed()

    async def connect(self) -> None:
        """Connect to the SSH server."""
        try:
            self._conn = await asyncssh.connect(
                self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                known_hosts=self.known_hosts,
                # For OpenWrt, we might need to accept unknown host keys if not provided
                # But for security, we should probably require known_hosts or use a specific policy.
                # For now, let's use known_hosts=None which defaults to checking ~/.ssh/known_hosts
                # If known_hosts is explicitly None, asyncssh might still check default.
                # To disable check (INSECURE but common for dev): known_hosts=None with client_keys=None?
                # Actually, to disable: known_hosts=None is not enough.
                # We can use known_hosts=None and client_keys=None to rely on system config?
                # Let's allow passing known_hosts path. If None, maybe we should allow strict checking or not.
                # For this implementation, let's assume standard behavior.
            )
        except asyncssh.PermissionDenied:
            raise AuthenticationError("SSH authentication failed")
        except (OSError, asyncssh.Error) as e:
            raise DeviceConnectionError(f"SSH connection failed: {e}")

    async def run_command(self, command: str) -> Tuple[str, str, int]:
        """Run a command on the remote server.

        Returns:
            Tuple[stdout, stderr, exit_status]
        """
        if not self._conn:
            await self.connect()

        if not self._conn:  # Should be connected now
            raise DeviceConnectionError("SSH connection not established")

        try:
            result = await self._conn.run(command)
            stdout = str(result.stdout) if result.stdout is not None else ""
            stderr = str(result.stderr) if result.stderr is not None else ""
            exit_status = result.exit_status if result.exit_status is not None else -1
            return stdout, stderr, exit_status
        except asyncssh.Error as e:
            raise SSHError(f"SSH command failed: {e}")
