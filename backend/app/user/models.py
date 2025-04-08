from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Index,
    String,
    Table,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ENUM, UUID

from app.models import metadata

User = Table(
    "users",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    ),
    Column("username", String(255), nullable=False, unique=True),
    Column("email", String(255), nullable=False, unique=True),
    Column("hashed_password", String(512), nullable=False),
    Column("is_admin", Boolean, nullable=False, server_default=text("false")),
    Column("current_client_id", ForeignKey("clients.id", ondelete="CASCADE"), nullable=True),
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
    Index("ix_users_username_created_at", "username", "created_at"),
    Index("ix_users_email_created_at", "email", "created_at"),
)

STATUS = ENUM("pending", "invited", "active", "deactivated", name="status")

Profile = Table(
    "profiles",
    metadata,
    Column(
        "client_id",
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    ),
    Column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    ),
    Column("is_client_owner", Boolean, nullable=False, server_default=text("false")),
    Column("avatar_url", String(512), nullable=True),
    Column("full_name", String(255), nullable=True),
    Column("status", STATUS, nullable=False, server_default=text("'pending'")),
    Column("last_login_at", TIMESTAMP(timezone=True), nullable=True),
    Column("created_at", TIMESTAMP, nullable=False, server_default=func.now()),
    Column(
        "updated_at",
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
    Index("ix_profiles_client_id", "client_id"),
    Index("ix_profiles_user_id", "user_id"),
)
