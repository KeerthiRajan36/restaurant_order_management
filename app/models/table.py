from sqlalchemy import Column, Integer, String, Enum

from sqlalchemy.orm import relationship

import enum

from app.database import Base

class TableStatus(str,enum.Enum):
    AVAILABLE = "Available"
    RESERVED = "Reserved"
    OCCUPIED = "Occupied"
    OUT_OF_SERVICE = "Out of Service" 

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer,primary_key=True,index=True)

    table_number = Column(
        String(20),
        unique=True,
        nullable=False
    )

    seating_capacity = Column(
        Integer,
        nullable=False
    )

    table_type = Column(
        String(50),
        nullable=False
    )

    status = Column(
        Enum(TableStatus),
        default=TableStatus.AVAILABLE
    )

    reservations = relationship(
        "Reservation",
        back_populates="table",
        cascade="all, delete"
    )