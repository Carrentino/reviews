from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository

from src.db.models.users import UserReviewReply


class UserReviewReplyRepository(ISqlAlchemyRepository[UserReviewReply]):
    _model = UserReviewReply
