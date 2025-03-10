from datetime import datetime
from decimal import Decimal
from uuid import UUID

from helpers.models.response import PaginatedResponse
from pydantic import BaseModel


class CarReviewReplySchema(BaseModel):
    id: UUID
    description: str
    created_at: datetime


class AuthorSchema(BaseModel):
    id: UUID
    first_name: str | None = None
    last_name: str | None = None


class CarReviewSchema(BaseModel):
    id: UUID
    author: AuthorSchema
    score: Decimal
    description: str
    car_id: UUID
    is_liked: bool
    likes_count: int
    created_at: datetime
    reply: CarReviewReplySchema | None = None


class CarReviewPaginatedResponse(PaginatedResponse):
    data: list[CarReviewSchema]
