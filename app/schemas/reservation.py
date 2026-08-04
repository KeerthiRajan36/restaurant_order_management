from pydantic import BaseModel, Field
from datetime import date
from datetime import time


class ReservationCreate(BaseModel):

    table_id: int

    reservation_date: date

    reservation_time: time

    number_of_guests: int = Field(..., gt=0)


class ReservationUpdate(BaseModel):

    status: str


class ReservationResponse(BaseModel):

    id: int

    customer_id: int

    table_id: int

    reservation_date: date

    reservation_time: time

    number_of_guests: int

    status: str

    class Config:
        from_attributes = True