from pydantic import BaseModel


class DailySalesReport(BaseModel):

    total_orders: int

    total_sales: float


class TableOccupancyReport(BaseModel):

    available: int

    reserved: int

    occupied: int

    out_of_service: int