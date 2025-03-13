from uuid import UUID

from helpers.models.response import PaginatedResponse

from src.web.api.schemas import ReviewSchema


class CarReviewSchema(ReviewSchema):
    car_id: UUID


class CarReviewPaginatedResponse(PaginatedResponse):
    data: list[CarReviewSchema]
