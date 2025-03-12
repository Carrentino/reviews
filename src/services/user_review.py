from src.integrations.users import UsersClient
from src.repositories.user_review import UserReviewRepository
from src.repositories.user_review_like import UserReviewLikeRepository
from src.repositories.user_review_reply import UserReviewReplyRepository
from src.services.base import BaseReviewService
from src.web.api.schemas import ReviewReplySchema, AuthorSchema
from src.web.api.users.schemas import UserReviewSchema


class UserReviewService(BaseReviewService):
    def __init__(
        self,
        user_review_repository: UserReviewRepository,
        user_review_like_repository: UserReviewLikeRepository,
        user_review_reply_repository: UserReviewReplyRepository,
        users_client: UsersClient,
    ) -> None:
        self.review_repository = user_review_repository
        self.user_review_like_repository = user_review_like_repository
        self.user_review_reply_repository = user_review_reply_repository
        self.users_client = users_client

    @staticmethod
    async def generate_schema(item: dict, author: AuthorSchema, reply: ReviewReplySchema) -> UserReviewSchema:
        return UserReviewSchema(
            id=item['review'].id,
            author=author,
            score=item['review'].score,
            description=item['review'].description,
            user_id=item['review'].user_id,
            created_at=item['review'].created_at,
            reply=reply,
            is_liked=item['is_liked'],
            likes_count=item['likes_count'],
        )
