from tortoise import fields
from tortoise.models import Model

class DashboardData(Model):
    id = fields.IntField(pk=True)
    hotel_id = fields.IntField()
    year = fields.IntField()
    month = fields.IntField()
    day = fields.IntField()
    bookings_count = fields.IntField()

    class Meta:
        table = "dashboard_data"
