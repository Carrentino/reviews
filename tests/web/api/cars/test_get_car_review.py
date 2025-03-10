from uuid import uuid4

from helpers.models.user import UserContext
from httpx import AsyncClient
from starlette import status

from tests.factories.car_review import CarReviewFactory
from tests.factories.car_review_like import CarReviewLikeFactory
from tests.factories.car_review_reply import CarReviewReplyFactory


async def test_get_car_reviews(user_context: UserContext, auth_client: AsyncClient):
    car_id = uuid4()
    review = await CarReviewFactory.create(car_id=car_id)

    await CarReviewLikeFactory.create(review=review, user_id=user_context.user_id)
    await CarReviewLikeFactory.create(review=review, user_id=uuid4())
    reply = await CarReviewReplyFactory.create(review=review)
    response = await auth_client.get(f'/api/cars/{car_id}/')
    assert response.status_code == status.HTTP_200_OK
    json_resp = response.json()

    assert json_resp['data'][0]['is_liked']
    assert json_resp['data'][0]['likes_count'] == 2
    assert json_resp['data'][0]['reply']['id'] == str(reply.id)
