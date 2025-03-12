import factory

from src.db.models.users import UserReviewReply
from tests.factories.base import BaseSqlAlchemyFactory


class UserReviewReplyFactory(BaseSqlAlchemyFactory):
    class Meta:
        model = UserReviewReply

    review = factory.SubFactory('tests.factories.user_review.UserReviewFactory')
    description = factory.Faker('text')
