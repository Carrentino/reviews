from decimal import Decimal
from uuid import UUID

from helpers.sqlalchemy.base_model import Base
from sqlalchemy.orm import Mapped


class BaseReview(Base):
    __abstract__ = True
    author_id: Mapped[UUID]
    score: Mapped[Decimal]
    description: Mapped[str]


class BaseReviewReply(Base):
    __abstract__ = True
    description: Mapped[str]


class BaseReviewLike(Base):
    __abstract__ = True
    user_id: Mapped[UUID]
