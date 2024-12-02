from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel
from math import ceil

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total_items: int
    page_number: Optional[int]
    page_size: Optional[int]
    total_pages: int

    @classmethod
    def create(cls, items: List[T], total_items: int, page_number: int, page_size: int) -> "PaginatedResponse[T]":
        total_pages = ceil(total_items / page_size) if page_size > 0 else 0
        return cls(
            items=items,
            total_items=total_items,
            page_number=page_number,
            page_size=page_size,
            total_pages=total_pages,
        )
