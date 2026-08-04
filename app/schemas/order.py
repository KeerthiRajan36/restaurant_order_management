from pydantic import BaseModel
from typing import List


class OrderItemCreate(BaseModel):

    menu_item_id: int

    quantity: int


class OrderCreate(BaseModel):

    reservation_id: int

    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):

    payment_status: str


class OrderItemResponse(BaseModel):

    id: int

    menu_item_id: int

    quantity: int

    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):

    id: int

    reservation_id: int

    total_amount: float

    payment_status: str

    items: List[OrderItemResponse]

    class Config:
        from_attributes = True