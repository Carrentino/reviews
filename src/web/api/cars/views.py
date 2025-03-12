from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from helpers.depends.auth import get_optional_user
from helpers.models.response import PaginatedResponse
from helpers.models.user import UserContext
from helpers.utils import get_paginated_response

from src.services.car_review import CarReviewService
from src.web.api.cars.schemas import CarReviewPaginatedResponse
from src.web.api.schemas import PaginationSchema
from src.web.depends.service import get_car_review_service

cars_router = APIRouter()


@cars_router.get('/{car_id}/', response_model=CarReviewPaginatedResponse)
async def get_car_reviews(
    car_review_service: Annotated[CarReviewService, Depends(get_car_review_service)],
    user_context: Annotated[UserContext | None, Depends(get_optional_user)],
    car_id: UUID,
    pagination: PaginationSchema = Depends(),
) -> PaginatedResponse:
    user_id = None if user_context is None else user_context.user_id
    result, total = await car_review_service.get_reviews(car_id, pagination, user_id)
    return await get_paginated_response(data=result, count=total, limit=pagination.limit, offset=pagination.offset)
