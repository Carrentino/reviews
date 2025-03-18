from uuid import uuid4

from httpx import AsyncClient
from starlette import status

from src.web.api.common.enums import ReviewType
from src.web.api.common.schemas import LikeReviewReq
from tests.factories.car_review import CarReviewFactory
from tests.factories.user_review import UserReviewFactory


async def test_like_car_review_ok(auth_client: AsyncClient) -> None:
    review = await CarReviewFactory.create()
    req = LikeReviewReq(
        type=ReviewType.CAR,
    )
    response = await auth_client.post(f'/api/common/review/{review.id}/like/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_like_car_review_nf(auth_client: AsyncClient) -> None:
    req = LikeReviewReq(
        type=ReviewType.CAR,
    )
    response = await auth_client.post(f'/api/common/review/{uuid4()}/like/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_like_user_review_ok(auth_client: AsyncClient) -> None:
    review = await UserReviewFactory.create()
    req = LikeReviewReq(
        type=ReviewType.USER,
    )
    response = await auth_client.post(f'/api/common/review/{review.id}/like/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_like_user_review_nf(auth_client: AsyncClient) -> None:
    review = await CarReviewFactory.create()
    req = LikeReviewReq(
        type=ReviewType.USER,
    )
    response = await auth_client.post(f'/api/common/review/{review.id}/like/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_404_NOT_FOUND
