from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.reservation import (
    Reservation,
    ReservationStatus
)

from app.models.table import (
    Table,
    TableStatus
)

from app.models.user import User

from app.schemas.reservation import (
    ReservationCreate,
    ReservationUpdate
)

from app.exceptions.custom_exceptions import (
    BusinessException,
    NotFoundException,
    ValidationException
)

from app.utils.pagination import paginate


class ReservationService:

    @staticmethod
    def create_reservation(
        db: Session,
        customer: User,
        request: ReservationCreate
    ):

        table = (
            db.query(Table)
            .filter(Table.id == request.table_id)
            .first()
        )

        if table is None:
            raise NotFoundException(
                "Table not found."
            )

        if table.status == TableStatus.OUT_OF_SERVICE:
            raise BusinessException(
                "Table is out of service."
            )

        if request.number_of_guests > table.seating_capacity:
            raise ValidationException(
                "Number of guests exceeds table capacity."
            )

        overlapping = (
            db.query(Reservation)
            .filter(
                and_(
                    Reservation.table_id == request.table_id,
                    Reservation.reservation_date == request.reservation_date,
                    Reservation.reservation_time == request.reservation_time,
                    Reservation.status != ReservationStatus.CANCELLED
                )
            )
            .first()
        )

        if overlapping:
            raise BusinessException(
                "Table already reserved for this time."
            )

        reservation = Reservation(
            customer_id=customer.id,
            table_id=request.table_id,
            reservation_date=request.reservation_date,
            reservation_time=request.reservation_time,
            number_of_guests=request.number_of_guests,
            status=ReservationStatus.RESERVED
        )

        table.status = TableStatus.RESERVED

        db.add(reservation)
        db.commit()
        db.refresh(reservation)

        return reservation

    @staticmethod
    def get_all_reservations(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        query = (
            db.query(Reservation)
            .order_by(
                Reservation.reservation_date.desc()
            )
        )

        return paginate(query, page, limit)

    @staticmethod
    def get_customer_reservations(
        db: Session,
        customer_id: int,
        page: int = 1,
        limit: int = 10
    ):

        query = (
            db.query(Reservation)
            .filter(
                Reservation.customer_id == customer_id
            )
            .order_by(
                Reservation.reservation_date.desc()
            )
        )

        return paginate(query, page, limit)

    @staticmethod
    def filter_by_status(
        db: Session,
        status: str,
        page: int = 1,
        limit: int = 10
    ):

        query = (
            db.query(Reservation)
            .filter(
                Reservation.status == status
            )
            .order_by(
                Reservation.reservation_date.desc()
            )
        )

        return paginate(query, page, limit)

    @staticmethod
    def update_reservation(
        db: Session,
        reservation_id: int,
        request: ReservationUpdate
    ):

        reservation = (
            db.query(Reservation)
            .filter(
                Reservation.id == reservation_id
            )
            .first()
        )

        if reservation is None:
            raise NotFoundException(
                "Reservation not found."
            )

        reservation.status = request.status

        table = (
            db.query(Table)
            .filter(
                Table.id == reservation.table_id
            )
            .first()
        )

        if request.status == ReservationStatus.CANCELLED:

            table.status = TableStatus.AVAILABLE

        elif request.status == ReservationStatus.SEATED:

            table.status = TableStatus.OCCUPIED

        elif request.status == ReservationStatus.COMPLETED:

            table.status = TableStatus.AVAILABLE

        db.commit()
        db.refresh(reservation)

        return reservation

    @staticmethod
    def get_reservation(
        db: Session,
        reservation_id: int
    ):

        reservation = (
            db.query(Reservation)
            .filter(
                Reservation.id == reservation_id
            )
            .first()
        )

        if reservation is None:
            raise NotFoundException(
                "Reservation not found."
            )

        return reservation

    @staticmethod
    def cancel_reservation(
        db: Session,
        reservation_id: int
    ):

        reservation = (
            db.query(Reservation)
            .filter(
                Reservation.id == reservation_id
            )
            .first()
        )

        if reservation is None:
            raise NotFoundException(
                "Reservation not found."
            )

        reservation.status = ReservationStatus.CANCELLED

        table = (
            db.query(Table)
            .filter(
                Table.id == reservation.table_id
            )
            .first()
        )

        table.status = TableStatus.AVAILABLE

        db.commit()

        return {
            "message": "Reservation cancelled successfully."
        }