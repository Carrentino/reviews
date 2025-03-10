from typing import Any
from uuid import UUID

import httpx
from helpers.clients.http_client import BaseApiClient


class UsersClient(BaseApiClient):
    _base_url = 'https://carrentino.ru/users'

    async def get_users(self, ids: list[UUID]) -> dict[UUID, dict[str, None]] | list[dict[Any, dict[str, Any]]]:
        url = f'{self._base_url}/api/users/'
        for user_id in ids:
            url += f'&user__id={user_id}'
        response = await self.get(url)
        result = {}
        try:
            response.raise_for_status()
        except httpx.HTTPError:
            for user_id in ids:
                result[user_id] = {'first_name': None, 'last_name': None}
            return result
        for item in response.json()['data']:
            result[item['id']] = {'first_name': item['first_name'], 'last_name': item['last_name']}
        return result
