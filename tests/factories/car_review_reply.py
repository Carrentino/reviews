import factory

from src.db.models.cars import CarReviewReply
from tests.factories.base import BaseSqlAlchemyFactory


class CarReviewReplyFactory(BaseSqlAlchemyFactory):
    class Meta:
        model = CarReviewReply

    review = factory.SubFactory('tests.factories.car_review.CarReviewFactory')
    description = factory.Faker('text')
