from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository

from src.db.models.users import UserReviewLike


class UserReviewLikeRepository(ISqlAlchemyRepository[UserReviewLike]):
    _model = UserReviewLike
