"""Pytest fixtures."""

import pytest
from sqlmodel import create_engine, SQLModel, Session
from openwrt_mcp.managers import DeviceManager


@pytest.fixture(name="session")
def session_fixture():
    """Create a new database session for a test."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="device_manager")
def device_manager_fixture():
    """Create a device manager with an in-memory database."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    return DeviceManager(engine)
