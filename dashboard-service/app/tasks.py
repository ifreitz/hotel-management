import requests
import asyncio

from datetime import datetime, timedelta
from celery import shared_task

from app.models import DashboardData
from app.database import init_db, close_db


DATA_PROVIDER_URL = "http://data-provider:8000/events"


@shared_task(name="update_dashboard")
def update_dashboard():
    """Fetch events from Data Provider"""
    asyncio.run(process_update())


async def process_update():
    """Process updating of dashboard data."""
    print("Updating dashboard....")

    await init_db()

    params = {
        "updated__gte": datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat(),
        "updated__lte": datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999).isoformat(),
    }
    response = requests.get(DATA_PROVIDER_URL, params=params)
    events = response.json()

    for event in events:
        event_timestamp = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
        print(event)
        print("Event timestamp year:", event_timestamp.year)
        print("Event timestamp month:", event_timestamp.month)
        print("Event timestamp day:", event_timestamp.day)
        existing_record = await DashboardData.filter(
            hotel_id=event['hotel_id'],
            year=event_timestamp.year,
            month=event_timestamp.month,
            day=event_timestamp.day,
        ).first()

        if existing_record:
            existing_record.bookings_count += 1 if event['rpg_status'] == 1 else 0
            await existing_record.save()
        else:
            await DashboardData.create(
                hotel_id=event['hotel_id'],
                year=event_timestamp.year,
                month=event_timestamp.month,
                day=event_timestamp.day,
                bookings_count=1 if event['rpg_status'] == 1 else 0
            )

    print("Dashboard updated")
    await close_db()
