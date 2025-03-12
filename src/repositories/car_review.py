from typing import TypedDict, Any
from uuid import UUID

from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository
from sqlalchemy import select, func, desc, asc
from sqlalchemy.orm import selectinload

from src.db.models.cars import CarReview, CarReviewLike
from src.web.api.enums import SortType, SortOrder
from src.web.api.schemas import PaginationSchema


class ReviewResult(TypedDict):
    review: CarReview
    likes_count: int
    is_liked: bool


class CarReviewRepository(ISqlAlchemyRepository[CarReview]):
    _model = CarReview

    async def get_reviews(
        self,
        car_id: UUID,
        pagination: PaginationSchema,
        user_id: UUID | None = None,
    ) -> tuple[list[dict[str, bool | Any]], Any | None]:
        likes_count = func.count(CarReviewLike.id).label("likes_count")
        is_liked = func.coalesce(func.bool_or(CarReviewLike.user_id == user_id), False).label("is_liked")

        query = (
            select(CarReview.id, CarReview, likes_count, is_liked)
            .where(CarReview.car_id == car_id)
            .outerjoin(CarReviewLike, CarReview.id == CarReviewLike.car_review_id)
            .options(selectinload(CarReview.reply))
            .group_by(CarReview.id)
        )

        if pagination.sort == SortType.POPULARITY:
            order_by = desc(likes_count) if pagination.sort_order == SortOrder.DESC else asc(likes_count)
        else:
            order_by = (
                desc(CarReview.created_at) if pagination.sort_order == SortOrder.DESC else asc(CarReview.created_at)
            )
        count_query = paginated_query = query
        count_query = select(func.count()).select_from(count_query.subquery().alias("subq"))
        paginated_query = paginated_query.order_by(order_by).limit(pagination.limit).offset(pagination.offset)

        result = await self.session.execute(paginated_query)

        count_result = await self.session.execute(count_query)
        total = count_result.scalar()

        reviews = []
        for row in result.unique().all():
            reviews.append(
                {
                    "review": row[1],  # Сам отзыв
                    "likes_count": row[2],  # Количество лайков
                    "is_liked": row[3] if user_id else False,
                }
            )

        return reviews, total
