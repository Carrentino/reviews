from typing import Any
from uuid import UUID

from src.integrations.users import UsersClient
from src.repositories.car_review import CarReviewRepository
from src.repositories.car_review_like import CarReviewLikeRepository
from src.repositories.car_review_reply import CarReviewReplyRepository
from src.web.api.cars.schemas import CarReviewReplySchema, CarReviewSchema, AuthorSchema
from src.web.api.schemas import PaginationSchema


class CarReviewService:
    def __init__(
        self,
        car_review_repository: CarReviewRepository,
        car_review_like_repository: CarReviewLikeRepository,
        car_review_reply_repository: CarReviewReplyRepository,
        users_client: UsersClient,
    ) -> None:
        self.car_review_repository = car_review_repository
        self.car_review_like_repository = car_review_like_repository
        self.car_review_reply_repository = car_review_reply_repository
        self.users_client = users_client

    async def get_reviews(
        self, car_id: UUID, pagination: PaginationSchema, user_id: UUID | None = None
    ) -> tuple[list[CarReviewSchema], Any | None]:
        reviews, total = await self.car_review_repository.get_reviews(car_id, pagination, user_id)
        result = []
        users = await self.users_client.get_users([item['review'].author_id for item in reviews])
        for item in reviews:
            if item['review'].reply is not None:
                reply = CarReviewReplySchema(
                    id=item['review'].reply.id,
                    description=item['review'].description,
                    created_at=item['review'].created_at,
                )
            else:
                reply = None
            author_id = item['review'].author_id
            author = AuthorSchema(
                id=author_id,
                first_name=users.get(author_id, {'first_name': None})['first_name'],
                last_name=users.get(author_id, {'last_name': None})['last_name'],
            )
            result.append(
                CarReviewSchema(
                    id=item['review'].id,
                    author=author,
                    score=item['review'].score,
                    description=item['review'].description,
                    car_id=item['review'].car_id,
                    created_at=item['review'].created_at,
                    reply=reply,
                    is_liked=item['is_liked'],
                    likes_count=item['likes_count'],
                )
            )
        return result, total
