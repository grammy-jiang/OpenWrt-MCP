"""Device manager."""

from typing import List, Optional
from sqlmodel import Session, select
from openwrt_mcp.db.models import Device
from openwrt_mcp.exceptions import DeviceNotFoundError


class DeviceManager:
    """Manager for Device registry."""

    def __init__(self, engine):
        self.engine = engine

    def create_device(
        self,
        name: str,
        host: str,
        username: str,
        password: str,
        port: int = 22,
        use_ssl: bool = False,
        description: Optional[str] = None,
    ) -> Device:
        """Create a new device."""
        with Session(self.engine) as session:
            device = Device(
                name=name,
                host=host,
                username=username,
                password=password,
                port=port,
                use_ssl=use_ssl,
                description=description,
            )
            session.add(device)
            session.commit()
            session.refresh(device)
            return device

    def get_device(self, name: str) -> Device:
        """Get a device by name."""
        with Session(self.engine) as session:
            statement = select(Device).where(Device.name == name)
            device = session.exec(statement).first()
            if not device:
                raise DeviceNotFoundError(f"Device '{name}' not found")
            return device

    def list_devices(self) -> List[Device]:
        """List all devices."""
        with Session(self.engine) as session:
            statement = select(Device)
            return list(session.exec(statement).all())

    def update_device(self, name: str, **kwargs) -> Device:
        """Update a device."""
        with Session(self.engine) as session:
            statement = select(Device).where(Device.name == name)
            device = session.exec(statement).first()
            if not device:
                raise DeviceNotFoundError(f"Device '{name}' not found")

            for key, value in kwargs.items():
                setattr(device, key, value)
            session.add(device)
            session.commit()
            session.refresh(device)
            return device

    def delete_device(self, name: str) -> None:
        """Delete a device."""
        with Session(self.engine) as session:
            statement = select(Device).where(Device.name == name)
            device = session.exec(statement).first()
            if not device:
                raise DeviceNotFoundError(f"Device '{name}' not found")

            session.delete(device)
            session.commit()
