from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import BaseReview, BaseReviewReply, BaseReviewLike


class CarReview(BaseReview):
    __tablename__ = "car_reviews"
    car_id: Mapped[UUID]

    reply: Mapped['CarReviewReply'] = relationship('CarReviewReply', back_populates='review')
    likes: Mapped[list['CarReviewLike']] = relationship('CarReviewLike', back_populates='review')


class CarReviewReply(BaseReviewReply):
    __tablename__ = 'car_review_replies'
    car_review_id: Mapped[UUID] = mapped_column(ForeignKey('car_reviews.id'), unique=True)

    review: Mapped['CarReview'] = relationship('CarReview', back_populates='reply')


class CarReviewLike(BaseReviewLike):
    __tablename__ = 'car_review_likes'
    car_review_id: Mapped[UUID] = mapped_column(ForeignKey('car_reviews.id'))

    review: Mapped['CarReview'] = relationship('CarReview', back_populates='likes')
