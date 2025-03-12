from uuid import uuid4

import factory

from src.db.models.cars import CarReview
from tests.factories.base import BaseSqlAlchemyFactory


class CarReviewFactory(BaseSqlAlchemyFactory):
    class Meta:
        model = CarReview

    car_id = factory.LazyAttribute(lambda _: uuid4())
    author_id = factory.LazyAttribute(lambda _: uuid4())
    score = factory.Faker('pydecimal', left_digits=1, right_digits=1, positive=True)
    description = factory.Faker('text')
