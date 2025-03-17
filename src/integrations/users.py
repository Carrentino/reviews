from typing import Any
from uuid import UUID

import httpx
from helpers.clients.http_client import BaseApiClient
from helpers.kafka.producer import KafkaProducer
from helpers.redis_client.client import RedisClient

from src.integrations.schemas.users import UsersChangeScoreSchema
from src.settings import get_settings


class UsersClient(BaseApiClient):
    _base_url = 'https://carrentino.ru/users'

    async def get_users(self, ids: list[UUID]) -> dict[UUID, dict[str, None]] | list[dict[Any, dict[str, Any]]]:
        url = f'{self._base_url}/api/users/'
        user_data = {}
        with RedisClient(address=get_settings().redis.url, db=get_settings().redis.users_db) as rc:
            for user_id in ids:
                data = await rc.get(user_id)
                if data is not None:
                    user_data[user_id] = data
                    continue
                url += f'&user__id={user_id}'
        response = await self.get(url)
        try:
            response.raise_for_status()
        except httpx.HTTPError:
            for user_id in ids:
                if user_id not in user_data:
                    user_data[user_id] = {'first_name': None, 'last_name': None}
            return user_data
        with RedisClient(address=get_settings().redis.url, db=get_settings().redis.users_db) as rc:
            for item in response.json()['data']:
                data = {'first_name': item['first_name'], 'last_name': item['last_name']}
                rc.set(item['id'], data)
                user_data[item['id']] = data
        return user_data


class UsersKafkaProducer(KafkaProducer):
    score_topic = get_settings().kafka.topic_users_score

    def __init__(self) -> None:
        super().__init__(str(get_settings().kafka.users_url))

    async def send_score(self, message: UsersChangeScoreSchema) -> None:
        await self.send_model_message(self.score_topic, message)
