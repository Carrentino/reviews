from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.web.api.schemas import ReviewReplySchema, AuthorSchema, ReviewSchema, PaginationSchema


class BaseReviewService(ABC):
    review_repository = None
    users_client = None

    @staticmethod
    @abstractmethod
    async def generate_schema(item: dict, author: AuthorSchema, reply: ReviewReplySchema) -> ReviewSchema: ...

    async def get_reviews(
        self, obj_review_id: UUID, pagination: PaginationSchema, current_user_id: UUID | None = None
    ) -> tuple[list[ReviewSchema], Any | None]:
        reviews, total = await self.review_repository.get_reviews(obj_review_id, pagination, current_user_id)
        result = []
        users = await self.users_client.get_users([item['review'].author_id for item in reviews])
        for item in reviews:
            if item['review'].reply is not None:
                reply = ReviewReplySchema(
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
            result.append(await self.generate_schema(item, author, reply))
        return result, total
