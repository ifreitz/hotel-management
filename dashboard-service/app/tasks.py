import requests
import asyncio

from datetime import datetime, timedelta
from celery import shared_task

from app.models import DashboardData, SyncSettings
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

    sync_setting = await SyncSettings.first()
    last_sync_timestamp = sync_setting.last_sync_timestamp if sync_setting else None

    params = {}

    if last_sync_timestamp:
        params["updated__gte"] = last_sync_timestamp.isoformat()
    
    response = requests.get(DATA_PROVIDER_URL, params=params)
    events = response.json()

    for event in events:
        event_timestamp = datetime.strptime(event['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
        
        existing_record = await DashboardData.filter(
            hotel_id=event['hotel_id'],
            year=event_timestamp.year,
            month=event_timestamp.month,
            day=event_timestamp.day,
        ).first()

        if existing_record:
            if event['rpg_status'] == 1:
                existing_record.bookings_count += 1
            else:
                existing_record.cancellations_count += 1

            await existing_record.save()
        else:
            await DashboardData.create(
                hotel_id=event['hotel_id'],
                year=event_timestamp.year,
                month=event_timestamp.month,
                day=event_timestamp.day,
                bookings_count=1 if event['rpg_status'] == 1 else 0,
                cancellations_count=0 if event['rpg_status'] == 1 else 1,
            )

    if len(events) > 0:
        if sync_setting:
            sync_setting.last_sync_timestamp = event_timestamp + timedelta(milliseconds=1)
            await sync_setting.save()
        else:
            await SyncSettings.create(last_sync_timestamp=event_timestamp)

    print("Dashboard updated")
    await close_db()
