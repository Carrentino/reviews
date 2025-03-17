from urllib.parse import urljoin
from uuid import UUID

from helpers.clients.http_client import BaseApiClient
from httpx import HTTPError

from src.settings import get_settings


class OrdersClient(BaseApiClient):
    _base_url = get_settings().orders_url

    async def get_renter_orders_by_car(self, car_id: UUID, token: str) -> dict:
        self.headers['X-Auth-Token'] = token
        url = urljoin(self._base_url, f'/renter-orders/?car_id={car_id}')
        response = await self.get(url)
        try:
            response.raise_for_status()
        except HTTPError:
            return {'total': 0}
        return response.json()

    async def get_lessor_orders_by_renter(self, renter_id: UUID, token: str) -> dict:
        self.headers['X-Auth-Token'] = token
        url = urljoin(self._base_url, f'/lessor-orders/?renter_id={renter_id}')
        response = await self.get(url)
        try:
            response.raise_for_status()
        except HTTPError:
            return {'total': 0}
        return response.json()
