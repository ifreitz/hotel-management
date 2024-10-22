from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url='postgres://data_provider_user:data_provider_password@data-provider-db:5432/data_provider_db',
        modules={'models': ['app.models']}
    )
    await Tortoise.generate_schemas()
