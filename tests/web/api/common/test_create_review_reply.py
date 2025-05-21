from unittest.mock import patch, AsyncMock
from uuid import uuid4, UUID

from helpers.models.user import UserContext
from httpx import AsyncClient
from starlette import status

from src.web.api.common.enums import ReviewType
from src.web.api.common.schemas import CreateReviewReplySchema
from tests.factories.car_review import CarReviewFactory
from tests.factories.user_review import UserReviewFactory


@patch('src.integrations.cars.CarsClient.get_car', new_callable=AsyncMock)
async def test_create_car_review_reply_ok(
    mock_get: AsyncMock, user_context: UserContext, auth_client: AsyncClient
) -> None:
    review = await CarReviewFactory.create()
    mock_get.return_value = {'owner_id': user_context.user_id}
    req = CreateReviewReplySchema(type=ReviewType.CAR, description='test')
    response = await auth_client.post(f'/api/common/review/{review.id}/reply/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_201_CREATED


@patch('src.integrations.cars.CarsClient.get_car', new_callable=AsyncMock)
async def test_create_car_review_reply_nf(
    mock_get: AsyncMock, user_context: UserContext, auth_client: AsyncClient
) -> None:
    mock_get.return_value = {'owner_id': user_context.user_id}
    req = CreateReviewReplySchema(type=ReviewType.CAR, review_id=uuid4(), description='test')
    response = await auth_client.post(f'/api/common/review/{uuid4()}/reply/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@patch('src.integrations.cars.CarsClient.get_car', new_callable=AsyncMock)
async def test_create_car_review_reply_fb(mock_get: AsyncMock, auth_client: AsyncClient) -> None:
    review = await CarReviewFactory.create()
    mock_get.return_value = {'owner_id': str(uuid4())}
    req = CreateReviewReplySchema(type=ReviewType.CAR, description='test')
    response = await auth_client.post(f'/api/common/review/{review.id}/reply/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_create_user_review_reply_ok(user_context: UserContext, auth_client: AsyncClient) -> None:
    review = await UserReviewFactory.create(user_id=UUID(user_context.user_id))
    req = CreateReviewReplySchema(type=ReviewType.USER, description='test')
    response = await auth_client.post(f'/api/common/review/{review.id}/reply/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_201_CREATED


async def test_create_user_review_reply_nf(auth_client: AsyncClient) -> None:
    req = CreateReviewReplySchema(type=ReviewType.USER, description='test')
    response = await auth_client.post(f'/api/common/review/{uuid4()}/reply/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_create_user_review_reply_fb(auth_client: AsyncClient) -> None:
    review = await UserReviewFactory.create()
    req = CreateReviewReplySchema(type=ReviewType.USER, description='test')
    response = await auth_client.post(f'/api/common/review/{review.id}/reply/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_403_FORBIDDEN
