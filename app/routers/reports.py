from datetime import date

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.orm import Session

from app.database import get_db

from app.services.report_service import ReportService

from app.utils.roles import (
    require_roles
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/daily-sales")
def daily_sales(
    report_date: date = Query(...),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "Admin",
            "Restaurant Manager"
        )
    )
):

    return ReportService.daily_sales_report(
        db,
        report_date
    )


@router.get("/table-occupancy")
def table_occupancy(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "Admin",
            "Restaurant Manager"
        )
    )
):

    return ReportService.table_occupancy_report(
        db
    )


@router.get("/reservation-status")
def reservation_status(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "Admin",
            "Restaurant Manager"
        )
    )
):

    return ReportService.reservation_status_report(
        db
    )


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "Admin",
            "Restaurant Manager"
        )
    )
):

    return ReportService.dashboard_summary(
        db
    )