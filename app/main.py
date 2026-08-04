from fastapi import FastAPI

from app.database import Base, engine

from app.routers.auth import router as auth_router
from app.routers.tables import router as table_router
from app.routers.menu import router as menu_router
from app.routers.reservations import router as reservation_router
from app.routers.orders import router as order_router
from app.routers.reports import router as report_router

from app.exceptions.handlers import register_exception_handlers

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurant Order & Table Reservation Management System"
    )

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(table_router)
app.include_router(menu_router)
app.include_router(reservation_router)
app.include_router(order_router)
app.include_router(report_router)


@app.get("/")
def root():
    return {
        "message": "Restaurant Order & Table Reservation Management API is running successfully."
    }