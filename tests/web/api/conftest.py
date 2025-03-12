from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from helpers.enums.auth import TokenType
from helpers.models.user import UserContext, UserStatus


@pytest.fixture()
async def user_context() -> UserContext:
    return UserContext(
        user_id=str(uuid4()), status=UserStatus.VERIFIED, type=TokenType.ACCESS, exp=datetime.now() + timedelta(days=7)
    )
