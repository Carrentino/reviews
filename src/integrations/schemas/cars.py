from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class CarsChangeScoreSchema(BaseModel):
    id: UUID
    score: Decimal
