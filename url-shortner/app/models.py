

from sqlmodel import SQLModel, Field, create_engine
from pydantic import HttpUrl
from datetime import datetime, timezone
from typing import Optional
import uuid

class URL(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    original_url: HttpUrl = Field(max_length=2048)  # Validates URLs
    short_code: str = Field(max_length=6, unique=True, nullable=False, index=True)  # Shortened for user-friendliness
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    clicks: int = Field(default=0, ge=0)  # Non-negative clicks

