from helpers.errors import BaseError


class UserHasNotOrderWithCarError(BaseError):
    message = "User has not order with this car"


class UserHasNotOrderWithUserError(BaseError):
    message = "User has not order with this user"


class ReviewNotFoundError(BaseError):
    message = "Review not found"


class UserIsNotOwnerError(BaseError):
    message = "User is not owner"
