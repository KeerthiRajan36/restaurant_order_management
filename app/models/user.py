from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
import enum

from app.database import Base

class UserRole(str,enum.Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    CUSTOMER = "Customer"


class User(Base): 

    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)

    full_name = Column(String(100),nullable=False)

    email = Column(String(255),unique=True,nullable=False,index=True)

    password = Column(String(255),nullable=False)

    role = Column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.CUSTOMER
        )

    reservations = relationship(
        "Reservation",
        back_populates="customer",
        cascade="all, delete"
    )

