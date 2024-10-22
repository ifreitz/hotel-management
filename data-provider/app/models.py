from tortoise import fields
from tortoise.models import Model

class Event(Model):
    id = fields.IntField(pk=True)
    hotel_id = fields.IntField()
    timestamp = fields.DatetimeField()
    rpg_status = fields.IntField()  # 1: booking, 2: cancellation
    room_id = fields.IntField()
    night_of_stay = fields.DateField()

    class Meta:
        table = "events"
