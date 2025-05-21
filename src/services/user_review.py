from uuid import UUID

from src.db.models.users import UserReview, UserReviewReply, UserReviewLike
from src.errors.service import UserHasNotOrderWithUserError, ReviewNotFoundError, UserIsNotOwnerError
from src.integrations.orders import OrdersClient
from src.integrations.schemas.users import UsersChangeScoreSchema
from src.integrations.users import UsersClient, UsersKafkaProducer
from src.repositories.user_review import UserReviewRepository
from src.repositories.user_review_like import UserReviewLikeRepository
from src.repositories.user_review_reply import UserReviewReplyRepository
from src.services.base import BaseReviewService
from src.web.api.common.enums import ReviewType
from src.web.api.common.schemas import CreateReviewResp, CreateReviewSchema, CreateReviewReplySchema
from src.web.api.schemas import ReviewReplySchema, AuthorSchema
from src.web.api.users.schemas import UserReviewSchema


class UserReviewService(BaseReviewService):
    def __init__(
        self,
        user_review_repository: UserReviewRepository,
        user_review_like_repository: UserReviewLikeRepository,
        user_review_reply_repository: UserReviewReplyRepository,
        users_client: UsersClient,
        orders_client: OrdersClient,
        users_kafka: UsersKafkaProducer,
    ) -> None:
        self.review_repository = user_review_repository
        self.user_review_like_repository = user_review_like_repository
        self.user_review_reply_repository = user_review_reply_repository
        self.users_client = users_client
        self.orders_client = orders_client
        self.users_kafka = users_kafka

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

    async def create_review(self, user_id: UUID, req: CreateReviewSchema, token: str) -> CreateReviewResp:
        orders = await self.orders_client.get_lessor_orders_by_renter(req.obj_id, token)
        if orders.get('total', 0) < 1:
            raise UserHasNotOrderWithUserError
        review = UserReview(
            user_id=req.obj_id,
            author_id=user_id,
            score=req.score,
            description=req.description,
        )
        review_id = await self.review_repository.create(review)
        change_score_msg = UsersChangeScoreSchema(id=req.obj_id, score=req.score)
        await self.users_kafka.send_score(change_score_msg)
        return CreateReviewResp(
            id=review_id,
            type=ReviewType.USER,
        )

    async def create_review_reply(
        self, user_id: UUID, req: CreateReviewReplySchema, review_id: UUID
    ) -> CreateReviewResp:
        review = await self.review_repository.get(review_id)
        if review is None:
            raise ReviewNotFoundError
        if review.user_id != user_id:
            raise UserIsNotOwnerError
        reply = UserReviewReply(
            user_review_id=review_id,
            description=req.description,
        )
        reply_id = await self.user_review_reply_repository.create(reply)
        return CreateReviewResp(
            id=reply_id,
            type=ReviewType.USER,
        )

    async def like_review(self, user_id: UUID, review_id: UUID) -> None:
        review = await self.review_repository.get(review_id)
        if review is None:
            raise ReviewNotFoundError
        review_like = await self.user_review_like_repository.get_one_by(user_id=user_id, user_review_id=review_id)
        if review_like is None:
            review_like = UserReviewLike(
                user_id=user_id,
                user_review_id=review_id,
            )
            await self.user_review_like_repository.create(review_like)
        else:
            await self.user_review_like_repository.delete(review_like.id)
