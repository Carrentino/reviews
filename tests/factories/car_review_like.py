from uuid import uuid4

import factory

from src.db.models.cars import CarReviewLike
from tests.factories.base import BaseSqlAlchemyFactory


class CarReviewLikeFactory(BaseSqlAlchemyFactory):
    class Meta:
        model = CarReviewLike

    review = factory.SubFactory('tests.factories.car_review.CarReviewFactory')
    user_id = factory.LazyAttribute(lambda _: uuid4())
