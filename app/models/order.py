from sqlalchemy import Column, Integer, Float, String, ForeignKey

from sqlalchemy.orm import relationship

from app.database import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer,primary_key=True,index=True)

    reservation_id = Column(
        Integer,
        ForeignKey("reservations.id"),
        unique=True
    )

    total_amount = Column(
        Float,
        default=0
    )

    payment_status = Column(
        String(50),
        default="Pending"
    )

    reservation = relationship(
        "Reservation",
        back_populates="order"
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete"
    )

