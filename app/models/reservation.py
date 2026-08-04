from sqlalchemy import Column, Integer, ForeignKey, Date, Time, Enum

from sqlalchemy.orm import relationship

import enum

from app.database import Base



class ReservationStatus(str,enum.Enum):
    RESERVED = "Reserved"
    SEATED = "Seated"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer,primary_key=True,index=True)

    customer_id = Column(Integer,ForeignKey("users.id"))

    table_id = Column(
        Integer,
        ForeignKey("tables.id")
    )

    reservation_date = Column(
        Date,
        nullable=False
    )

    reservation_time = Column(
        Time,
        nullable=False
    )

    number_of_guests = Column(
        Integer,
        nullable=False
    )

    status =  Column(
        Enum(ReservationStatus),
        default=ReservationStatus.RESERVED
    )

    customer = relationship(
        "User",
        back_populates="reservations"
    )

    table = relationship(
        "Table",
        back_populates="reservations"
    )

    order = relationship(
        "Order",
        back_populates="reservation",
        uselist=False,
        cascade="all, delete"
    )

