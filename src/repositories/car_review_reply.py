from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository

from src.db.models.cars import CarReviewReply


class CarReviewReplyRepository(ISqlAlchemyRepository[CarReviewReply]):
    _model = CarReviewReply
