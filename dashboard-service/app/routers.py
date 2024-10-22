from fastapi import APIRouter
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

    class Config:
        orm_mode = True

@router.get("/dashboard", response_model=List[DashboardSchema])
async def get_dashboard(hotel_id: int, year: int, period: str):
    """
    Get the dashboard data for a given hotel and period.
    period: "month" or "day"
    """
    if period == "month":
        data = await DashboardData.filter(hotel_id=hotel_id, year=year).group_by("month").all()
    elif period == "day":
        data = await DashboardData.filter(hotel_id=hotel_id, year=year).group_by("day").all()
    else:
        return []

    return data
