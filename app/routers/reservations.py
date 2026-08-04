from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.reservation import (
    ReservationCreate,
    ReservationUpdate,
    ReservationResponse
)

from app.services.reservation_service import ReservationService

from app.utils.roles import (
    get_current_user,
    require_roles
)

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)


@router.post(
    "",
    response_model=ReservationResponse,
    status_code=201
)
def create_reservation(
    request: ReservationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles("Customer")
    )
):

    return ReservationService.create_reservation(
        db,
        current_user,
        request
    )


@router.get("")
def get_reservations(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role.value == "Customer":

        return ReservationService.get_customer_reservations(
            db,
            current_user.id,
            page,
            limit
        )

    return ReservationService.get_all_reservations(
        db,
        page,
        limit
    )


@router.get(
    "/status/{status}"
)
def get_by_status(
    status: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "Admin",
            "Restaurant Manager"
        )
    )
):

    return ReservationService.filter_by_status(
        db,
        status,
        page,
        limit
    )


@router.get(
    "/{reservation_id}",
    response_model=ReservationResponse
)
def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    reservation = ReservationService.get_reservation(
        db,
        reservation_id
    )

    if (
        current_user.role.value == "Customer"
        and
        reservation.customer_id != current_user.id
    ):
        raise PermissionError(
            "Access denied."
        )

    return reservation


@router.put(
    "/{reservation_id}",
    response_model=ReservationResponse
)
def update_reservation(
    reservation_id: int,
    request: ReservationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "Admin",
            "Restaurant Manager"
        )
    )
):

    return ReservationService.update_reservation(
        db,
        reservation_id,
        request
    )


@router.delete(
    "/{reservation_id}"
)
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    reservation = ReservationService.get_reservation(
        db,
        reservation_id
    )

    if (
        current_user.role.value == "Customer"
        and
        reservation.customer_id != current_user.id
    ):
        raise PermissionError(
            "Access denied."
        )

    return ReservationService.cancel_reservation(
        db,
        reservation_id
    )