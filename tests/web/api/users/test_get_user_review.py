from unittest.mock import patch, AsyncMock
from uuid import uuid4

from helpers.models.user import UserContext
from httpx import AsyncClient
from starlette import status

from tests.factories.user_review import UserReviewFactory
from tests.factories.user_review_like import UserReviewLikeFactory
from tests.factories.user_review_reply import UserReviewReplyFactory


@patch('src.integrations.users.UsersClient.get_users', new_callable=AsyncMock)
async def test_get_user_reviews(mock_get_users: AsyncMock, user_context: UserContext, auth_client: AsyncClient):
    user_id = uuid4()
    review = await UserReviewFactory.create(user_id=user_id)

    likes = [
        await UserReviewLikeFactory.create(review=review, user_id=user_context.user_id),
        await UserReviewLikeFactory.create(review=review, user_id=uuid4()),
    ]
    mock_get_users.return_value = {
        likes[0].user_id: {'first_name': None, 'last_name': None},
        likes[1].user_id: {'first_name': None, 'last_name': None},
    }
    reply = await UserReviewReplyFactory.create(review=review)
    response = await auth_client.get(f'/api/users/{user_id}/')
    assert response.status_code == status.HTTP_200_OK
    json_resp = response.json()

    assert json_resp['data'][0]['is_liked']
    assert json_resp['data'][0]['likes_count'] == 2
    assert json_resp['data'][0]['reply']['id'] == str(reply.id)
