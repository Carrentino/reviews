from uuid import UUID

from src.db.models.cars import CarReview
from src.errors.service import UserHasNotOrderWithCarError
from src.integrations.cars import CarsKafkaProducer
from src.integrations.orders import OrdersClient
from src.integrations.schemas.cars import CarsChangeScoreSchema
from src.integrations.users import UsersClient
from src.repositories.car_review import CarReviewRepository
from src.repositories.car_review_like import CarReviewLikeRepository
from src.repositories.car_review_reply import CarReviewReplyRepository
from src.services.base import BaseReviewService
from src.web.api.cars.schemas import CarReviewSchema
from src.web.api.common.enums import ReviewType
from src.web.api.common.schemas import CreateReviewSchema, CreateReviewResp
from src.web.api.schemas import ReviewReplySchema, AuthorSchema


class CarReviewService(BaseReviewService):
    def __init__(
        self,
        car_review_repository: CarReviewRepository,
        car_review_like_repository: CarReviewLikeRepository,
        car_review_reply_repository: CarReviewReplyRepository,
        users_client: UsersClient,
        orders_client: OrdersClient,
        cars_kafka: CarsKafkaProducer,
    ) -> None:
        self.review_repository = car_review_repository
        self.car_review_like_repository = car_review_like_repository
        self.car_review_reply_repository = car_review_reply_repository
        self.users_client = users_client
        self.orders_client = orders_client
        self.cars_kafka = cars_kafka

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

    async def create_review(self, user_id: UUID, req: CreateReviewSchema, token: str) -> CreateReviewResp:
        orders = await self.orders_client.get_renter_orders_by_car(req.obj_id, token)
        if orders.get('total', 0) < 1:
            raise UserHasNotOrderWithCarError
        review = CarReview(
            car_id=req.obj_id,
            author_id=user_id,
            score=req.score,
            description=req.description,
        )
        review_id = await self.review_repository.create(review)
        change_score_msg = CarsChangeScoreSchema(id=req.obj_id, score=req.score)
        await self.cars_kafka.send_score(change_score_msg)
        return CreateReviewResp(
            id=review_id,
            type=ReviewType.CAR,
        )
