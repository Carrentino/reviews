from enum import StrEnum


class SortType(StrEnum):
    CREATED = 'created'
    POPULARITY = 'popularity'


class SortOrder(StrEnum):
    ASC = 'asc'
    DESC = 'desc'
