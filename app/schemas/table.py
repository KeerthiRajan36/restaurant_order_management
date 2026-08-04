from pydantic import BaseModel, Field
from typing import Optional


class TableCreate(BaseModel):
    table_number: str

    seating_capacity: int = Field(..., gt=0)

    table_type: str

    status: str = "Available"


class TableUpdate(BaseModel):
    seating_capacity: Optional[int] = Field(None, gt=0)

    table_type: Optional[str]

    status: Optional[str]


class TableResponse(BaseModel):
    id: int
    table_number: str
    seating_capacity: int
    table_type: str
    status: str

    class Config:
        from_attributes = True