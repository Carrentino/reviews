from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import BaseReview, BaseReviewReply, BaseReviewLike


class UserReview(BaseReview):
    __tablename__ = "user_reviews"
    user_id: Mapped[UUID]

    reply: Mapped['UserReviewReply'] = relationship('UserReviewReply', back_populates='review')
    likes: Mapped[list['UserReviewLike']] = relationship('UserReviewLike', back_populates='review')


class UserReviewReply(BaseReviewReply):
    __tablename__ = 'user_review_replies'
    user_review_id: Mapped[UUID] = mapped_column(ForeignKey('user_reviews.id'), unique=True)

    review: Mapped['UserReview'] = relationship('UserReview', back_populates='reply')


class UserReviewLike(BaseReviewLike):
    __tablename__ = 'user_review_likes'
    user_review_id: Mapped[UUID] = mapped_column(ForeignKey('user_reviews.id'))

    review: Mapped['UserReview'] = relationship('UserReview', back_populates='likes')
