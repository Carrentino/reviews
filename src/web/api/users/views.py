from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from helpers.depends.auth import get_optional_user
from helpers.models.response import PaginatedResponse
from helpers.models.user import UserContext
from helpers.utils import get_paginated_response

from src.services.user_review import UserReviewService
from src.web.api.schemas import PaginationSchema
from src.web.api.users.schemas import UserReviewPaginatedResponse
from src.web.depends.service import get_user_review_service

users_router = APIRouter()


@users_router.get('/{user_id}/', response_model=UserReviewPaginatedResponse)
async def get_car_reviews(
    user_review_service: Annotated[UserReviewService, Depends(get_user_review_service)],
    user_context: Annotated[UserContext | None, Depends(get_optional_user)],
    user_id: UUID,
    pagination: PaginationSchema = Depends(),
) -> PaginatedResponse:
    custom_user_id = None if user_context is None else user_context.user_id
    result, total = await user_review_service.get_reviews(user_id, pagination, custom_user_id)
    return await get_paginated_response(data=result, count=total, limit=pagination.limit, offset=pagination.offset)
