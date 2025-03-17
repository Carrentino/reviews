from helpers.kafka.producer import KafkaProducer

from src.integrations.schemas.cars import CarsChangeScoreSchema
from src.settings import get_settings


class CarsKafkaProducer(KafkaProducer):
    score_topic = get_settings().kafka.topic_cars_score

    def __init__(self) -> None:
        super().__init__(str(get_settings().kafka.cars_url))

    async def send_score(self, message: CarsChangeScoreSchema) -> None:
        await self.send_model_message(self.score_topic, message)
