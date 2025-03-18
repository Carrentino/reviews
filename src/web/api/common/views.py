from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from helpers.depends.auth import get_current_user
from helpers.models.user import UserContext
from starlette import status
from starlette.requests import Request

from src.errors.http import (
    IncorrectReviewTypeHttpError,
    UserHasNotOrderWithCarHttpError,
    UserHasNotOrderWithUserHttpError,
)
from src.errors.service import UserHasNotOrderWithCarError, UserHasNotOrderWithUserError
from src.services.car_review import CarReviewService
from src.services.user_review import UserReviewService
from src.web.api.common.enums import ReviewType
from src.web.api.common.schemas import CreateReviewSchema
from src.web.depends.service import get_car_review_service, get_user_review_service

common_router = APIRouter()


@common_router.post('/review/', status_code=status.HTTP_201_CREATED)
async def create_review(
    request: Request,
    car_review_service: Annotated[CarReviewService, Depends(get_car_review_service)],
    user_review_service: Annotated[UserReviewService, Depends(get_user_review_service)],
    user_context: Annotated[UserContext, Depends(get_current_user)],
    req: CreateReviewSchema,
):
    token = request.headers.get('X-Auth-Token')
    if req.type == ReviewType.CAR:
        try:
            return await car_review_service.create_review(UUID(user_context.user_id), req, token)
        except UserHasNotOrderWithCarError:
            raise UserHasNotOrderWithCarHttpError from None
    if req.type == ReviewType.USER:
        try:
            return await user_review_service.create_review(UUID(user_context.user_id), req, token)
        except UserHasNotOrderWithUserError:
            raise UserHasNotOrderWithUserHttpError from None
    raise IncorrectReviewTypeHttpError
