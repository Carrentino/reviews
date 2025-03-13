from src.integrations.users import UsersClient
from src.repositories.car_review import CarReviewRepository
from src.repositories.car_review_like import CarReviewLikeRepository
from src.repositories.car_review_reply import CarReviewReplyRepository
from src.services.base import BaseReviewService
from src.web.api.cars.schemas import CarReviewSchema
from src.web.api.schemas import ReviewReplySchema, AuthorSchema


class CarReviewService(BaseReviewService):
    def __init__(
        self,
        car_review_repository: CarReviewRepository,
        car_review_like_repository: CarReviewLikeRepository,
        car_review_reply_repository: CarReviewReplyRepository,
        users_client: UsersClient,
    ) -> None:
        self.review_repository = car_review_repository
        self.car_review_like_repository = car_review_like_repository
        self.car_review_reply_repository = car_review_reply_repository
        self.users_client = users_client

    @staticmethod
    async def generate_schema(item: dict, author: AuthorSchema, reply: ReviewReplySchema) -> CarReviewSchema:
        return CarReviewSchema(
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
