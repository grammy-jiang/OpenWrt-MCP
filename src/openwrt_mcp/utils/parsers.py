"""Output parsers for CLI tools."""

from typing import Dict, Any
import re


def parse_ping(output: str) -> Dict[str, Any]:
    """Parse ping output."""
    # Example output:
    # PING 8.8.8.8 (8.8.8.8): 56 data bytes
    # 64 bytes from 8.8.8.8: seq=0 ttl=118 time=13.456 ms
    # ...
    # --- 8.8.8.8 ping statistics ---
    # 5 packets transmitted, 5 packets received, 0% packet loss
    # round-trip min/avg/max = 13.456/14.200/15.123 ms

    stats: Dict[str, Any] = {}

    # Parse statistics
    match = re.search(
        r"(\d+) packets transmitted, (\d+) packets received, (\d+)% packet loss", output
    )
    if match:
        stats["transmitted"] = int(match.group(1))
        stats["received"] = int(match.group(2))
        stats["packet_loss_percent"] = int(match.group(3))

    match = re.search(
        r"round-trip min/avg/max = ([\d\.]+)/([\d\.]+)/([\d\.]+) ms", output
    )
    if match:
        stats["min_rtt"] = float(match.group(1))
        stats["avg_rtt"] = float(match.group(2))
        stats["max_rtt"] = float(match.group(3))

    return stats


def parse_iwinfo(output: str) -> Dict[str, Any]:
    """Parse iwinfo output."""
    # Placeholder for iwinfo parsing
    return {"raw": output}
