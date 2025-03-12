from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from src.web.api.enums import SortType, SortOrder


class PaginationSchema(BaseModel):
    limit: int = Field(30, ge=1, description='Количество')
    offset: int = Field(0, ge=0, description='Смещение')
    sort: SortType = SortType.POPULARITY
    sort_order: SortOrder = SortOrder.DESC


class ReviewReplySchema(BaseModel):
    id: UUID
    description: str
    created_at: datetime


class AuthorSchema(BaseModel):
    id: UUID
    first_name: str | None = None
    last_name: str | None = None


class ReviewSchema(BaseModel):
    id: UUID
    author: AuthorSchema
    score: Decimal
    description: str
    is_liked: bool
    likes_count: int
    created_at: datetime
    reply: ReviewReplySchema | None = None
