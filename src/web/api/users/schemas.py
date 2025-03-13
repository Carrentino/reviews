from uuid import UUID

from helpers.models.response import PaginatedResponse

from src.web.api.schemas import ReviewSchema


class UserReviewSchema(ReviewSchema):
    user_id: UUID


class UserReviewPaginatedResponse(PaginatedResponse):
    data: list[UserReviewSchema]
