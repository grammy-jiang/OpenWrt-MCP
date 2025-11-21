"""Configuration settings for OpenWrt MCP Server."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Database
    DB_NAME: str = "openwrt_mcp.db"
    DB_PATH: Path = Path.home() / ".openwrt-mcp" / DB_NAME

    # Logging
    LOG_LEVEL: str = "INFO"

    # Security (Optional default credentials if needed, though usually per-device)
    # DEFAULT_USERNAME: str = "root"
    # DEFAULT_PASSWORD: str = "password"

    model_config = SettingsConfigDict(env_prefix="OPENWRT_MCP_", env_file=".env")

    @property
    def database_url(self) -> str:
        """Get the database URL."""
        return f"sqlite:///{self.DB_PATH}"

    def ensure_db_dir(self) -> None:
        """Ensure the database directory exists."""
        self.DB_PATH.parent.mkdir(parents=True, exist_ok=True)


settings = Settings()
