"""Database models."""

from typing import Optional
from sqlmodel import Field, SQLModel


class Device(SQLModel, table=True):  # type: ignore
    """Device model representing an OpenWrt router."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    host: str
    username: str
    password: str  # In a real app, this should be encrypted or stored securely
    port: int = 22
    use_ssl: bool = False
    description: Optional[str] = None
