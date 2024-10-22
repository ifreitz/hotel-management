from fastapi import FastAPI

from app.routers import router
from app.database import init_db

app = FastAPI(
    title="Dashboard Service API",
    description="API to view hotel booking data on a monthly and daily basis",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(router)
