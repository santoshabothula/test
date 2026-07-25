import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Date, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
class Base(DeclarativeBase): pass
class MetadataEntity(Base):
    __tablename__="metadata"
    id: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label: Mapped[str]=mapped_column(String(200), index=True)
    description: Mapped[str]=mapped_column(String(2000), default="")
    start_date: Mapped[object|None]=mapped_column(Date, nullable=True)
    end_date: Mapped[object|None]=mapped_column(Date, nullable=True)
    data_versioning: Mapped[bool]=mapped_column(Boolean, default=False)
    metadata_version: Mapped[int]=mapped_column(Integer, default=1)
    status: Mapped[int]=mapped_column(Integer, default=4)
    api_visibility: Mapped[int]=mapped_column(Integer, default=1)
    template: Mapped[dict]=mapped_column(JSONB, default=dict)
    fields: Mapped[list]=mapped_column(JSONB, default=list)
    actions: Mapped[list]=mapped_column(JSONB, default=list)
    rules: Mapped[list]=mapped_column(JSONB, default=list)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
class SubmissionEntity(Base):
    __tablename__="submissions"
    id: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metadata_id: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True), ForeignKey("metadata.id", ondelete="CASCADE"), index=True)
    metadata_version: Mapped[int]=mapped_column(Integer)
    payload: Mapped[dict]=mapped_column(JSONB)
    submitted_by: Mapped[str]=mapped_column(String(200))
    submitted_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=datetime.utcnow)
