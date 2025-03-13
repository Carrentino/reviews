from uuid import uuid4

import factory

from src.db.models.users import UserReviewLike
from tests.factories.base import BaseSqlAlchemyFactory


class UserReviewLikeFactory(BaseSqlAlchemyFactory):
    class Meta:
        model = UserReviewLike

    review = factory.SubFactory('tests.factories.user_review.UserReviewFactory')
    user_id = factory.LazyAttribute(lambda _: uuid4())
