from sqlalchemy.orm import Session, joinedload

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.menu import Menu
from app.models.reservation import (
    Reservation,
    ReservationStatus
)

from app.schemas.order import (
    OrderCreate,
    OrderUpdate
)

from app.exceptions.custom_exceptions import (
    NotFoundException,
    BusinessException,
    ValidationException
)

from app.utils.pagination import paginate


class OrderService:

    @staticmethod
    def create_order(
        db: Session,
        request: OrderCreate
    ):

        reservation = (
            db.query(Reservation)
            .filter(
                Reservation.id == request.reservation_id
            )
            .first()
        )

        if reservation is None:
            raise NotFoundException(
                "Reservation not found."
            )

        if reservation.status == ReservationStatus.CANCELLED:
            raise BusinessException(
                "Cannot create order for cancelled reservation."
            )

        existing_order = (
            db.query(Order)
            .filter(
                Order.reservation_id == request.reservation_id
            )
            .first()
        )

        if existing_order:
            raise BusinessException(
                "Order already exists for this reservation."
            )

        order = Order(
            reservation_id=request.reservation_id,
            total_amount=0,
            payment_status="Pending"
        )

        db.add(order)
        db.flush()

        total = 0

        for item in request.items:

            if item.quantity <= 0:
                raise ValidationException(
                    "Quantity must be greater than zero."
                )

            menu_item = (
                db.query(Menu)
                .filter(Menu.id == item.menu_item_id)
                .first()
            )

            if menu_item is None:
                raise NotFoundException(
                    f"Menu item {item.menu_item_id} not found."
                )

            if not menu_item.availability:
                raise BusinessException(
                    f"{menu_item.item_name} is unavailable."
                )

            subtotal = menu_item.price * item.quantity

            total += subtotal

            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=menu_item.id,
                quantity=item.quantity,
                price=menu_item.price
            )

            db.add(order_item)

        order.total_amount = total

        db.commit()

        db.refresh(order)

        return order

    @staticmethod
    def get_orders(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        query = (
            db.query(Order)
            .options(
                joinedload(Order.items)
            )
            .order_by(Order.id.desc())
        )

        return paginate(
            query,
            page,
            limit
        )

    @staticmethod
    def get_order(
        db: Session,
        order_id: int
    ):

        order = (
            db.query(Order)
            .options(
                joinedload(Order.items)
            )
            .filter(
                Order.id == order_id
            )
            .first()
        )

        if order is None:
            raise NotFoundException(
                "Order not found."
            )

        return order

    @staticmethod
    def update_order(
        db: Session,
        order_id: int,
        request: OrderUpdate
    ):

        order = (
            db.query(Order)
            .filter(
                Order.id == order_id
            )
            .first()
        )

        if order is None:
            raise NotFoundException(
                "Order not found."
            )

        reservation = (
            db.query(Reservation)
            .filter(
                Reservation.id == order.reservation_id
            )
            .first()
        )

        if reservation.status == ReservationStatus.COMPLETED:
            raise BusinessException(
                "Completed orders cannot be modified."
            )

        order.payment_status = request.payment_status

        db.commit()

        db.refresh(order)

        return order

    @staticmethod
    def get_customer_orders(
        db: Session,
        customer_id: int,
        page: int = 1,
        limit: int = 10
    ):

        query = (
            db.query(Order)
            .join(Reservation)
            .filter(
                Reservation.customer_id == customer_id
            )
            .options(
                joinedload(Order.items)
            )
            .order_by(Order.id.desc())
        )

        return paginate(
            query,
            page,
            limit
        )