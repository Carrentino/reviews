from typing import Annotated

from fastapi import Depends

from src.integrations.users import UsersClient
from src.repositories.car_review import CarReviewRepository
from src.repositories.car_review_like import CarReviewLikeRepository
from src.repositories.car_review_reply import CarReviewReplyRepository
from src.services.car_review import CarReviewService
from src.web.depends.integrations import get_users_client
from src.web.depends.repository import (
    get_car_review_repository,
    get_car_review_reply_repository,
    get_car_review_like_repository,
)


async def get_car_review_service(
    car_review_repository: Annotated[CarReviewRepository, Depends(get_car_review_repository)],
    car_review_like_repository: Annotated[CarReviewLikeRepository, Depends(get_car_review_like_repository)],
    car_review_reply_repository: Annotated[CarReviewReplyRepository, Depends(get_car_review_reply_repository)],
    users_client: Annotated[UsersClient, Depends(get_users_client)],
) -> CarReviewService:
    return CarReviewService(
        car_review_repository=car_review_repository,
        car_review_like_repository=car_review_like_repository,
        car_review_reply_repository=car_review_reply_repository,
        users_client=users_client,
    )
