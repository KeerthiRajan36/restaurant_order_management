from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse
)

from app.services.order_service import OrderService

from app.utils.roles import (
    get_current_user,
    require_roles
)

from app.exceptions.custom_exceptions import (
    ForbiddenException
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "",
    response_model=OrderResponse,
    status_code=201
)
def create_order(
    request: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "Admin",
            "Restaurant Manager"
        )
    )
):

    return OrderService.create_order(
        db,
        request
    )


@router.get("")
def get_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role.value == "Customer":

        return OrderService.get_customer_orders(
            db,
            current_user.id,
            page,
            limit
        )

    return OrderService.get_orders(
        db,
        page,
        limit
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    order = OrderService.get_order(
        db,
        order_id
    )

    if current_user.role.value == "Customer":

        if (
            order.reservation.customer_id
            != current_user.id
        ):
            raise ForbiddenException(
                "You are not allowed to access this order."
            )

    return order


@router.put(
    "/{order_id}",
    response_model=OrderResponse
)
def update_order(
    order_id: int,
    request: OrderUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "Admin",
            "Restaurant Manager"
        )
    )
):

    return OrderService.update_order(
        db,
        order_id,
        request
    )