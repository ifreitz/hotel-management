import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.models import DashboardData

router = APIRouter()

class DashboardSchema(BaseModel):
    hotel_id: int
    year: int
    month: Optional[int]
    day: Optional[int]
    bookings_count: int
    cancellations_count: int

    class Config:
        orm_mode = True

@router.get("/dashboard", response_model=DashboardSchema)
async def get_dashboard(hotel_id: int, period: datetime.date, filter_by: str = "month"):
    """
    Retrieves dashboard data for a specified hotel and period. The period is expected in YYYY-MM-DD format. \n
    The filter_by parameter allows for filtering by 'month', or 'day'. If 'month' is provided, data is filtered for the whole month.
    If 'day' is provided, data is filtered for the whole day.
    """
    if filter_by == "month":
        data = await DashboardData.filter(hotel_id=hotel_id, year=period.year, month=period.month).all()
    elif filter_by == "day":
        data = await DashboardData.filter(hotel_id=hotel_id, year=period.year, month=period.month, day=period.day).all()
    else:
        raise HTTPException(status_code=400, detail="Invalid filter_by parameter. Must be 'month' or 'day'.")

    # Aggregate bookings and cancellations
    bookings_count = sum(item.bookings_count for item in data)
    cancellations_count = sum(item.cancellations_count for item in data)

    return DashboardSchema(
        hotel_id=hotel_id,
        year=period.year,
        month=period.month,
        day=period.day,
        bookings_count=bookings_count,
        cancellations_count=cancellations_count,
    )
