from urllib.parse import urljoin
from uuid import UUID

from helpers.clients.http_client import BaseApiClient
from helpers.kafka.producer import KafkaProducer
from httpx import HTTPError

from src.integrations.schemas.cars import CarsChangeScoreSchema
from src.settings import get_settings


class CarsKafkaProducer(KafkaProducer):
    score_topic = get_settings().kafka.topic_cars_score

    def __init__(self) -> None:
        super().__init__(str(get_settings().kafka.cars_url))

    async def send_score(self, message: CarsChangeScoreSchema) -> None:
        await self.send_model_message(self.score_topic, message)


class CarsClient(BaseApiClient):
    _base_url = get_settings().cars_url

    async def get_car(self, car_id: UUID) -> dict:
        url = urljoin(self._base_url, f'/listings/?car__id={car_id}')
        response = await self.get(url)
        try:
            response.raise_for_status()
        except HTTPError:
            return {}
        return response.json()
