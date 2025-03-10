from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository

from src.db.models.cars import CarReviewLike


class CarReviewLikeRepository(ISqlAlchemyRepository[CarReviewLike]):
    _model = CarReviewLike
