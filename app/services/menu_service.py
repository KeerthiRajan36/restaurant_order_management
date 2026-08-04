from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.menu import Menu

from app.schemas.menu import (
    MenuCreate,
    MenuUpdate
)

from app.exceptions.custom_exceptions import (
    NotFoundException
)

from app.utils.pagination import paginate


class MenuService:

    @staticmethod
    def create_menu_item(
        db: Session,
        request: MenuCreate
    ):

        menu_item = Menu(
            item_name=request.item_name,
            category=request.category,
            price=request.price,
            availability=request.availability
        )

        db.add(menu_item)
        db.commit()
        db.refresh(menu_item)

        return menu_item

    @staticmethod
    def get_all_menu(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        query = (
            db.query(Menu)
            .order_by(Menu.item_name)
        )

        return paginate(
            query=query,
            page=page,
            limit=limit
        )

    @staticmethod
    def get_menu_item(
        db: Session,
        item_id: int
    ):

        item = (
            db.query(Menu)
            .filter(Menu.id == item_id)
            .first()
        )

        if item is None:
            raise NotFoundException(
                "Menu item not found."
            )

        return item

    @staticmethod
    def update_menu_item(
        db: Session,
        item_id: int,
        request: MenuUpdate
    ):

        item = (
            db.query(Menu)
            .filter(Menu.id == item_id)
            .first()
        )

        if item is None:
            raise NotFoundException(
                "Menu item not found."
            )

        if request.item_name is not None:
            item.item_name = request.item_name

        if request.category is not None:
            item.category = request.category

        if request.price is not None:
            item.price = request.price

        if request.availability is not None:
            item.availability = request.availability

        db.commit()
        db.refresh(item)

        return item

    @staticmethod
    def delete_menu_item(
        db: Session,
        item_id: int
    ):

        item = (
            db.query(Menu)
            .filter(Menu.id == item_id)
            .first()
        )

        if item is None:
            raise NotFoundException(
                "Menu item not found."
            )

        db.delete(item)
        db.commit()

        return {
            "message": "Menu item deleted successfully."
        }

    @staticmethod
    def search_menu(
        db: Session,
        keyword: str,
        page: int = 1,
        limit: int = 10
    ):

        query = (
            db.query(Menu)
            .filter(
                or_(
                    Menu.item_name.ilike(f"%{keyword}%"),
                    Menu.category.ilike(f"%{keyword}%")
                )
            )
            .order_by(Menu.item_name)
        )

        return paginate(
            query=query,
            page=page,
            limit=limit
        )

    @staticmethod
    def available_menu(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        query = (
            db.query(Menu)
            .filter(Menu.availability == True)
            .order_by(Menu.item_name)
        )

        return paginate(
            query=query,
            page=page,
            limit=limit
        )