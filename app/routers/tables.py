from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.table import (
    TableCreate,
    TableUpdate,
    TableResponse
)

from app.services.table_service import TableService

from app.utils.roles import (
    get_current_user,
    require_roles
)

router = APIRouter(
    prefix="/tables",
    tags=["Tables"]
)


@router.post(
    "",
    response_model=TableResponse,
    status_code=201
)
def create_table(
    request: TableCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "Admin",
            "Restaurant Manager"
        )
    )
):
    return TableService.create_table(
        db,
        request
    )


@router.get("")
def get_tables(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return TableService.get_all_tables(
        db,
        page,
        limit
    )


@router.get(
    "/{table_id}",
    response_model=TableResponse
)
def get_table(
    table_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return TableService.get_table(
        db,
        table_id
    )


@router.put(
    "/{table_id}",
    response_model=TableResponse
)
def update_table(
    table_id: int,
    request: TableUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "Admin",
            "Restaurant Manager"
        )
    )
):

    return TableService.update_table(
        db,
        table_id,
        request
    )


@router.delete("/{table_id}")
def delete_table(
    table_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "Admin"
        )
    )
):

    return TableService.delete_table(
        db,
        table_id
    )