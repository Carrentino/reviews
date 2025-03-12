from pydantic import BaseModel, Field

from src.web.api.enums import SortType, SortOrder


class PaginationSchema(BaseModel):
    limit: int = Field(30, ge=1, description='Количество')
    offset: int = Field(0, ge=0, description='Смещение')
    sort: SortType = SortType.POPULARITY
    sort_order: SortOrder = SortOrder.DESC
