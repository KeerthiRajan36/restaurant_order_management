from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.reservation import (
    Reservation,
    ReservationStatus
)
from app.models.table import (
    Table,
    TableStatus
)


class ReportService:

    @staticmethod
    def daily_sales_report(
        db: Session,
        report_date: date
    ):

        total_orders = (
            db.query(Order)
            .join(Reservation)
            .filter(
                Reservation.reservation_date == report_date
            )
            .count()
        )

        total_sales = (
            db.query(
                func.coalesce(
                    func.sum(Order.total_amount),
                    0
                )
            )
            .join(Reservation)
            .filter(
                Reservation.reservation_date == report_date
            )
            .scalar()
        )

        return {
            "report_date": report_date,
            "total_orders": total_orders,
            "total_sales": float(total_sales)
        }

    @staticmethod
    def table_occupancy_report(
        db: Session
    ):

        available = (
            db.query(Table)
            .filter(
                Table.status == TableStatus.AVAILABLE
            )
            .count()
        )

        reserved = (
            db.query(Table)
            .filter(
                Table.status == TableStatus.RESERVED
            )
            .count()
        )

        occupied = (
            db.query(Table)
            .filter(
                Table.status == TableStatus.OCCUPIED
            )
            .count()
        )

        out_of_service = (
            db.query(Table)
            .filter(
                Table.status == TableStatus.OUT_OF_SERVICE
            )
            .count()
        )

        return {
            "available": available,
            "reserved": reserved,
            "occupied": occupied,
            "out_of_service": out_of_service
        }

    @staticmethod
    def reservation_status_report(
        db: Session
    ):

        reserved = (
            db.query(Reservation)
            .filter(
                Reservation.status == ReservationStatus.RESERVED
            )
            .count()
        )

        seated = (
            db.query(Reservation)
            .filter(
                Reservation.status == ReservationStatus.SEATED
            )
            .count()
        )

        completed = (
            db.query(Reservation)
            .filter(
                Reservation.status == ReservationStatus.COMPLETED
            )
            .count()
        )

        cancelled = (
            db.query(Reservation)
            .filter(
                Reservation.status == ReservationStatus.CANCELLED
            )
            .count()
        )

        return {
            "reserved": reserved,
            "seated": seated,
            "completed": completed,
            "cancelled": cancelled
        }

    @staticmethod
    def dashboard_summary(
        db: Session
    ):

        return {

            "total_tables":
                db.query(Table).count(),

            "total_reservations":
                db.query(Reservation).count(),

            "completed_orders":
                db.query(Order).count(),

            "today_sales":
                float(
                    db.query(
                        func.coalesce(
                            func.sum(
                                Order.total_amount
                            ),
                            0
                        )
                    )
                    .join(Reservation)
                    .filter(
                        Reservation.reservation_date == date.today()
                    )
                    .scalar()
                )
        }