from sqlalchemy import Column, Integer, String, Float, Boolean

from sqlalchemy.orm import relationship

from app.database import Base


class Menu(Base):

    __tablename__ = "menu"

    id = Column(Integer,primary_key=True,index=True)

    item_name = Column(
        String(120),
        nullable=False,
        index=True    
    )

    category = Column(
        String(80),
        nullable=False,
        index=True
    )

    price = Column(
        Float,
        nullable=False
    )

    availablity = Column(
        Boolean,
        default=True
    )

    order_items = relationship(
        "OrderItem",
        back_populates="menu_item"
    )
    