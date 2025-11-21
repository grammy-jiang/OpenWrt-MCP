"""Database engine and session management."""

from sqlmodel import create_engine, SQLModel, Session
from openwrt_mcp.config import settings

engine = create_engine(settings.database_url)


def init_db():
    """Initialize the database."""
    settings.ensure_db_dir()
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a database session."""
    with Session(engine) as session:
        yield session
