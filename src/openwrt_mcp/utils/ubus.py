"""Async Ubus JSON-RPC client."""

import httpx
import json
from typing import Any, Dict, Optional, List
from openwrt_mcp.exceptions import UbusError, AuthenticationError, DeviceConnectionError


class UbusClient:
    """Client for interacting with OpenWrt via Ubus JSON-RPC."""

    def __init__(
        self, base_url: str, username: str, password: str, verify_ssl: bool = False
    ):
        self.base_url = base_url.rstrip("/")
        self.rpc_url = f"{self.base_url}/ubus"
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self.session_id: Optional[str] = None
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(verify=self.verify_ssl, timeout=10.0)
        await self.login()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()

    async def _request(self, method: str, params: List[Any]) -> Dict[str, Any]:
        """Send a JSON-RPC request."""
        if not self._client:
            self._client = httpx.AsyncClient(verify=self.verify_ssl, timeout=10.0)

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }

        try:
            response = await self._client.post(self.rpc_url, json=payload)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError as e:
            raise DeviceConnectionError(f"Failed to connect to {self.base_url}: {e}")
        except json.JSONDecodeError:
            raise DeviceConnectionError(f"Invalid JSON response from {self.base_url}")

        if "error" in data and data["error"]:
            # Ubus JSON-RPC errors usually have a code and message?
            # Actually, standard JSON-RPC has 'error' object.
            # OpenWrt ubus sometimes returns 'result': [code] where code != 0
            error = data["error"]
            if isinstance(error, dict):
                raise UbusError(
                    error.get("code", -1), error.get("message", "Unknown error")
                )
            else:
                raise UbusError(-1, str(error))

        # Check for ubus specific result codes in the result array
        # Usually result is [return_data] or [code]
        # If method is "call", result is [return_data]
        # If method is "login", result is [session_id] or [0, session_id] depending on version?
        # Let's handle standard ubus response.

        return data

    async def login(self) -> None:
        """Login to Ubus and get a session ID."""
        # session.login is the ubus object and method
        # But via JSON-RPC, the method is "call" usually: call(session_id, "session", "login", {...})
        # Wait, initial login is special.
        # The JSON-RPC endpoint supports "call", "list", "get", etc.
        # To login, we usually use "call" with a dummy session ID (00000000000000000000000000000000)
        # or use the "login" method if exposed directly?
        # Standard OpenWrt rpcd exposes "session" object.

        # Correct way:
        # POST /ubus
        # { "jsonrpc": "2.0", "id": 1, "method": "call", "params": ["00000000000000000000000000000000", "session", "login", {"username": "root", "password": "password"}] }

        params = [
            "00000000000000000000000000000000",
            "session",
            "login",
            {"username": self.username, "password": self.password},
        ]

        data = await self._request("call", params)

        # Result is usually [return_code, { "ubus_rpc_session": "..." }] or just [{...}]
        # If successful, result[1] contains the session data.
        # Wait, ubus call returns [result_dict] usually.

        result = data.get("result")
        if not result or not isinstance(result, list):
            raise AuthenticationError("Invalid login response format")

        # Check for error code in result[0] if it's an integer?
        # Usually for "call", if successful, it returns [data].
        # If failed, it might return nothing or error is in 'error' field of JSON-RPC.

        # Let's assume result[0] is the data if success.
        session_data = result[1] if len(result) > 1 else result[0]

        if isinstance(session_data, int):
            # This is an error code
            raise AuthenticationError(f"Login failed with code {session_data}")

        if "ubus_rpc_session" in session_data:
            self.session_id = session_data["ubus_rpc_session"]
        else:
            raise AuthenticationError("No session ID in login response")

    async def call(
        self, object_path: str, method: str, args: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        """Call a Ubus method."""
        if not self.session_id:
            await self.login()

        params = [self.session_id, object_path, method, args]
        data = await self._request("call", params)

        result = data.get("result")
        if not result or not isinstance(result, list):
            # This might happen if void return?
            return {}

        # result[0] is usually the return code (0 for success) in some versions, or the data.
        # Actually, for "call", result is [data].
        # If there is an error, 'error' field in JSON-RPC response is set?
        # Or result is [code] where code != 0.

        if len(result) == 1:
            if isinstance(result[0], int) and result[0] != 0:
                raise UbusError(result[0], "Ubus call failed")
            return result[0]
        elif len(result) == 2:
            # [code, data] ?
            if isinstance(result[0], int) and result[0] != 0:
                raise UbusError(result[0], "Ubus call failed")
            return result[1]

        return {}

    async def list(self, path: str = "*") -> List[str]:
        """List available Ubus objects."""
        if not self.session_id:
            await self.login()

        params = [self.session_id, path]
        data = await self._request("list", params)

        result = data.get("result")
        if result and isinstance(result, list):
            return result
        return []
