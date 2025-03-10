from typing import Any
from uuid import UUID

import httpx
from helpers.clients.http_client import BaseApiClient
from helpers.redis_client.client import RedisClient

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
