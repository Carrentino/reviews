from typing import Any
from uuid import UUID

from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository
from sqlalchemy import func, select, desc, asc
from sqlalchemy.orm import selectinload

from src.db.models.users import UserReview, UserReviewLike
from src.web.api.enums import SortOrder, SortType
from src.web.api.schemas import PaginationSchema


class UserReviewRepository(ISqlAlchemyRepository[UserReview]):
    _model = UserReview

    async def get_reviews(
        self,
        user_id: UUID,
        pagination: PaginationSchema,
        current_user_id: UUID | None = None,
    ) -> tuple[list[dict[str, bool | Any]], Any | None]:
        likes_count = func.count(UserReviewLike.id).label("likes_count")
        is_liked = func.coalesce(func.bool_or(UserReviewLike.user_id == current_user_id), False).label("is_liked")

        query = (
            select(UserReview.id, UserReview, likes_count, is_liked)
            .where(UserReview.user_id == user_id)
            .outerjoin(UserReviewLike, UserReview.id == UserReviewLike.user_review_id)
            .options(selectinload(UserReview.reply))
            .group_by(UserReview.id)
        )

        if pagination.sort == SortType.POPULARITY:
            order_by = desc(likes_count) if pagination.sort_order == SortOrder.DESC else asc(likes_count)
        else:
            order_by = (
                desc(UserReview.created_at) if pagination.sort_order == SortOrder.DESC else asc(UserReview.created_at)
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
                    "review": row[1],
                    "likes_count": row[2],
                    "is_liked": row[3] if current_user_id else False,
                }
            )

        return reviews, total
