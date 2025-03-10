from typing import Annotated

from fastapi import Depends
from helpers.depends.db_session import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.car_review import CarReviewRepository
from src.repositories.car_review_like import CarReviewLikeRepository
from src.repositories.car_review_reply import CarReviewReplyRepository


async def get_car_review_repository(session: Annotated[AsyncSession, Depends(get_db_session)]) -> CarReviewRepository:
    return CarReviewRepository(session)


async def get_car_review_like_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> CarReviewLikeRepository:
    return CarReviewLikeRepository(session)


async def get_car_review_reply_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> CarReviewReplyRepository:
    return CarReviewReplyRepository(session)
