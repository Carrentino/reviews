from decimal import Decimal
from unittest.mock import patch, AsyncMock
from uuid import uuid4

from httpx import AsyncClient
from starlette import status

from src.integrations.schemas.cars import CarsChangeScoreSchema
from src.integrations.schemas.users import UsersChangeScoreSchema
from src.web.api.common.enums import ReviewType
from src.web.api.common.schemas import CreateReviewSchema


@patch('src.integrations.orders.OrdersClient.get_renter_orders_by_car', new_callable=AsyncMock)
@patch('src.integrations.cars.CarsKafkaProducer.send_score', new_callable=AsyncMock)
async def test_create_car_review_ok(mock_send: AsyncMock, mock_get: AsyncMock, auth_client: AsyncClient) -> None:
    req = CreateReviewSchema(
        type=ReviewType.CAR,
        obj_id=uuid4(),
        score=Decimal('5.0'),
        description='',
    )
    mock_get.return_value = {'total': 1}
    change_score_msg = CarsChangeScoreSchema(id=req.obj_id, score=req.score)
    response = await auth_client.post('/api/common/review/', json=req.model_dump(mode='json'))
    mock_send.assert_called_once_with(change_score_msg)
    assert response.status_code == status.HTTP_201_CREATED


@patch('src.integrations.orders.OrdersClient.get_renter_orders_by_car', new_callable=AsyncMock)
@patch('src.integrations.cars.CarsKafkaProducer.send_score', new_callable=AsyncMock)
async def test_create_car_review_fb(mock_send: AsyncMock, mock_get: AsyncMock, auth_client: AsyncClient) -> None:
    req = CreateReviewSchema(
        type=ReviewType.CAR,
        obj_id=uuid4(),
        score=Decimal('5.0'),
        description='',
    )
    mock_get.return_value = {'total': 0}
    response = await auth_client.post('/api/common/review/', json=req.model_dump(mode='json'))
    mock_send.assert_not_called()
    assert response.status_code == status.HTTP_403_FORBIDDEN


@patch('src.integrations.orders.OrdersClient.get_lessor_orders_by_renter', new_callable=AsyncMock)
@patch('src.integrations.users.UsersKafkaProducer.send_score', new_callable=AsyncMock)
async def test_create_user_review_ok(mock_send: AsyncMock, mock_get: AsyncMock, auth_client: AsyncClient) -> None:
    req = CreateReviewSchema(
        type=ReviewType.USER,
        obj_id=uuid4(),
        score=Decimal('5.0'),
        description='',
    )
    mock_get.return_value = {'total': 1}
    change_score_msg = UsersChangeScoreSchema(id=req.obj_id, score=req.score)
    response = await auth_client.post('/api/common/review/', json=req.model_dump(mode='json'))
    mock_send.assert_called_once_with(change_score_msg)
    assert response.status_code == status.HTTP_201_CREATED


@patch('src.integrations.orders.OrdersClient.get_lessor_orders_by_renter', new_callable=AsyncMock)
@patch('src.integrations.users.UsersKafkaProducer.send_score', new_callable=AsyncMock)
async def test_create_user_review_fb(mock_send: AsyncMock, mock_get: AsyncMock, auth_client: AsyncClient) -> None:
    req = CreateReviewSchema(
        type=ReviewType.USER,
        obj_id=uuid4(),
        score=Decimal('5.0'),
        description='',
    )
    mock_get.return_value = {'total': 0}
    response = await auth_client.post('/api/common/review/', json=req.model_dump(mode='json'))
    mock_send.assert_not_called()
    assert response.status_code == status.HTTP_403_FORBIDDEN
