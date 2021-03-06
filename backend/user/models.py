from tortoise import fields, models


class User(models.Model):
    id = fields.IntField(
        pk=True
    )
    username = fields.CharField(
        max_length=128,
        unique=True
    )
    password = fields.CharField(
        max_length=512,
    )
    email = fields.CharField(
        max_length=128,
        unique=True
    )
    is_active = fields.BooleanField(
        default=False
    )
    join_date = fields.DatetimeField(
        auto_now_add=True
    )

    def __str__(self) -> str:
        return f"User {self.id}: {self.username}, {self.email}"

    class PydanticMeta:
        # Let's exclude the created timestamp
        exclude = ("password",)
