from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url='postgres://dashboard_service_user:dashboard_service_password@dashboard-service-db:5432/dashboard_service_db',
        modules={'models': ['app.models']}
    )
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()
