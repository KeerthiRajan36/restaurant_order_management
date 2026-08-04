from pydantic import BaseModel, Field
from typing import Optional


class MenuCreate(BaseModel):
    item_name: str

    category: str

    price: float = Field(..., gt=0)

    availability: bool = True


class MenuUpdate(BaseModel):
    item_name: Optional[str]

    category: Optional[str]

    price: Optional[float] = Field(None, gt=0)

    availability: Optional[bool]


class MenuResponse(BaseModel):
    id: int
    item_name: str
    category: str
    price: float
    availability: bool

    class Config:
        from_attributes = True