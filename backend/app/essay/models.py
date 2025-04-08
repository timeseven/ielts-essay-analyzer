from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    Numeric,
    String,
    Table,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ENUM, UUID

from app.models import metadata

Category = Table(
    "essay_categories",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        autoincrement=True,
    ),
    Column("name", String(255), nullable=False, index=True),
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
    Column("deleted_at", TIMESTAMP(timezone=True), nullable=True),
)

TaskType = ENUM("task_1", "task_2", name="tasktype")

Question = Table(
    "essay_questions",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    ),
    Column("content", Text, nullable=False),
    Column("task_type", TaskType, nullable=False, server_default="task_1"),
    Column(
        "category_id",
        ForeignKey("essay_categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    ),
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
    Column("deleted_at", TIMESTAMP(timezone=True), nullable=True),
)


Essay = Table(
    "essay_contents",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    ),
    Column("client_id", UUID(as_uuid=True), nullable=False),
    Column("owner_id", UUID(as_uuid=True), nullable=False),
    Column(
        "question_id",
        ForeignKey("essay_questions.id", ondelete="SET NULL"),
        nullable=True,
    ),
    Column("content", Text, nullable=False),
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
    Column("deleted_at", TIMESTAMP(timezone=True), nullable=True),
    Index("ix_essays_client_id", "client_id"),
    Index("ix_essays_owner_id", "owner_id"),
    ForeignKeyConstraint(
        ["client_id", "owner_id"],
        ["profiles.client_id", "profiles.user_id"],
        ondelete="CASCADE",
    ),
)

Assessment = Table(
    "essay_assessments",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    ),
    Column(
        "essay_id",
        ForeignKey("essay_contents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column("client_id", UUID(as_uuid=True), nullable=False),
    Column("owner_id", UUID(as_uuid=True), nullable=False),
    Column("overall_score", Numeric(precision=2, scale=1), nullable=False),
    Column("overall_score_feedback", Text, nullable=False),
    Column("task_achievement", Numeric(precision=2, scale=1), nullable=False),
    Column("task_achievement_feedback", Text, nullable=False),
    Column("coherence_cohesion", Numeric(precision=2, scale=1), nullable=False),
    Column("coherence_cohesion_feedback", Text, nullable=False),
    Column("lexical_resource", Numeric(precision=2, scale=1), nullable=False),
    Column("lexical_resource_feedback", Text, nullable=False),
    Column("grammatical_range", Numeric(precision=2, scale=1), nullable=False),
    Column("grammatical_range_feedback", Text, nullable=False),
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
    CheckConstraint("overall_score >= 0 AND overall_score <= 9", name="check_overall_score_range"),
    CheckConstraint(
        "task_achievement >= 0 AND task_achievement <= 9",
        name="check_task_achievement_range",
    ),
    CheckConstraint(
        "coherence_cohesion >= 0 AND coherence_cohesion <= 9",
        name="check_coherence_cohesion_range",
    ),
    CheckConstraint(
        "lexical_resource >= 0 AND lexical_resource <= 9",
        name="check_lexical_resource_range",
    ),
    CheckConstraint(
        "grammatical_range >= 0 AND grammatical_range <= 9",
        name="check_grammatical_range_range",
    ),
    ForeignKeyConstraint(
        ["client_id", "owner_id"],
        ["profiles.client_id", "profiles.user_id"],
        ondelete="CASCADE",
    ),
)
