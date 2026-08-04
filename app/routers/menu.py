from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.menu import (
    MenuCreate,
    MenuUpdate,
    MenuResponse
)

from app.services.menu_service import MenuService

from app.utils.roles import (
    get_current_user,
    require_roles
)

router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)


@router.post(
    "",
    response_model=MenuResponse,
    status_code=201
)
def create_menu_item(
    request: MenuCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "Admin",
            "Restaurant Manager"
        )
    )
):

    return MenuService.create_menu_item(
        db,
        request
    )


@router.get("")
def get_menu(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return MenuService.get_all_menu(
        db,
        page,
        limit
    )


@router.get("/search")
def search_menu(
    keyword: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return MenuService.search_menu(
        db,
        keyword,
        page,
        limit
    )


@router.get("/available")
def available_menu(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return MenuService.available_menu(
        db,
        page,
        limit
    )


@router.get(
    "/{item_id}",
    response_model=MenuResponse
)
def get_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return MenuService.get_menu_item(
        db,
        item_id
    )


@router.put(
    "/{item_id}",
    response_model=MenuResponse
)
def update_menu_item(
    item_id: int,
    request: MenuUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "Admin",
            "Restaurant Manager"
        )
    )
):

    return MenuService.update_menu_item(
        db,
        item_id,
        request
    )


@router.delete("/{item_id}")
def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "Admin"
        )
    )
):

    return MenuService.delete_menu_item(
        db,
        item_id
    )