from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from src.web.api.common.enums import ReviewType


class CreateReviewSchema(BaseModel):
    type: ReviewType
    obj_id: UUID
    score: Decimal
    description: str


class CreateReviewResp(BaseModel):
    id: UUID
    type: ReviewType


class CreateReviewReplySchema(BaseModel):
    type: ReviewType
    review_id: UUID
    description: str
