from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class UsersChangeScoreSchema(BaseModel):
    id: UUID
    score: Decimal
