"""Tests for DeviceManager."""

from openwrt_mcp.managers import DeviceManager
from openwrt_mcp.exceptions import DeviceNotFoundError
import pytest


def test_create_device(device_manager: DeviceManager):
    """Test creating a device."""
    device = device_manager.create_device(
        name="router1", host="192.168.1.1", username="root", password="password"
    )
    assert device.id is not None
    assert device.name == "router1"
    assert device.host == "192.168.1.1"


def test_get_device(device_manager: DeviceManager):
    """Test getting a device."""
    device_manager.create_device(
        name="router1", host="192.168.1.1", username="root", password="password"
    )
    device = device_manager.get_device("router1")
    assert device.name == "router1"


def test_get_device_not_found(device_manager: DeviceManager):
    """Test getting a non-existent device."""
    with pytest.raises(DeviceNotFoundError):
        device_manager.get_device("nonexistent")


def test_list_devices(device_manager: DeviceManager):
    """Test listing devices."""
    device_manager.create_device(name="d1", host="h1", username="u", password="p")
    device_manager.create_device(name="d2", host="h2", username="u", password="p")
    devices = device_manager.list_devices()
    assert len(devices) == 2


def test_update_device(device_manager: DeviceManager):
    """Test updating a device."""
    device_manager.create_device(name="d1", host="h1", username="u", password="p")
    updated = device_manager.update_device("d1", host="h1_updated")
    assert updated.host == "h1_updated"

    fetched = device_manager.get_device("d1")
    assert fetched.host == "h1_updated"


def test_delete_device(device_manager: DeviceManager):
    """Test deleting a device."""
    device_manager.create_device(name="d1", host="h1", username="u", password="p")
    device_manager.delete_device("d1")
    with pytest.raises(DeviceNotFoundError):
        device_manager.get_device("d1")
