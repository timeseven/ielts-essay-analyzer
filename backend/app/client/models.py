from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    String,
    Table,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID

from app.models import metadata


Client = Table(
    "clients",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    ),
    Column("name", String(255), nullable=False),
    Column("created_at", TIMESTAMP, nullable=False, server_default=func.now()),
    Column(
        "updated_at",
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
)
