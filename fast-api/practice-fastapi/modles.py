
from pydantic import BaseModel, Field
from typing import Optional, Literal

# class Item(BaseModel):
#     id : int


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class ItemNew(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []