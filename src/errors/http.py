from helpers.errors import ServerError
from starlette import status


class IncorrectReviewTypeHttpError(ServerError):
    message = "Incorrect Review Type"
    status_code = status.HTTP_400_BAD_REQUEST


class UserHasNotOrderWithCarHttpError(ServerError):
    message = "User has not order with this car"
    status_code = status.HTTP_403_FORBIDDEN


class UserHasNotOrderWithUserHttpError(ServerError):
    message = "User has not order with this user"
    status_code = status.HTTP_403_FORBIDDEN
