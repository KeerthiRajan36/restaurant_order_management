from sqlalchemy.orm import Session

from app.models.table import Table

from app.schemas.table import (
    TableCreate,
    TableUpdate
)

from app.exceptions.custom_exceptions import (
    AlreadyExistsException,
    NotFoundException
)

from app.utils.pagination import paginate


class TableService:

    @staticmethod
    def create_table(
        db: Session,
        request: TableCreate
    ):

        existing = (
            db.query(Table)
            .filter(
                Table.table_number == request.table_number
            )
            .first()
        )

        if existing:
            raise AlreadyExistsException(
                "Table number already exists."
            )

        table = Table(
            table_number=request.table_number,
            seating_capacity=request.seating_capacity,
            table_type=request.table_type,
            status=request.status
        )

        db.add(table)
        db.commit()
        db.refresh(table)

        return table

    @staticmethod
    def get_all_tables(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        query = (
            db.query(Table)
            .order_by(Table.table_number)
        )

        return paginate(
            query=query,
            page=page,
            limit=limit
        )

    @staticmethod
    def get_table(
        db: Session,
        table_id: int
    ):

        table = (
            db.query(Table)
            .filter(Table.id == table_id)
            .first()
        )

        if table is None:
            raise NotFoundException(
                "Table not found."
            )

        return table

    @staticmethod
    def update_table(
        db: Session,
        table_id: int,
        request: TableUpdate
    ):

        table = (
            db.query(Table)
            .filter(Table.id == table_id)
            .first()
        )

        if table is None:
            raise NotFoundException(
                "Table not found."
            )

        if request.seating_capacity is not None:
            table.seating_capacity = (
                request.seating_capacity
            )

        if request.table_type is not None:
            table.table_type = request.table_type

        if request.status is not None:
            table.status = request.status

        db.commit()
        db.refresh(table)

        return table

    @staticmethod
    def delete_table(
        db: Session,
        table_id: int
    ):

        table = (
            db.query(Table)
            .filter(Table.id == table_id)
            .first()
        )

        if table is None:
            raise NotFoundException(
                "Table not found."
            )

        db.delete(table)
        db.commit()

        return {
            "message": "Table deleted successfully."
        }