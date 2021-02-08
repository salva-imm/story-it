from tortoise import fields, models


class Story(models.Model):
    id = fields.IntField(
        pk=True
    )
    user = fields.ForeignKeyField(
        model_name="models.User",
        related_name="stories",
        null=True,
        on_delete=fields.SET_NULL
    )
    email = fields.CharField(
        max_length=128
    )
    is_active = fields.BooleanField(
        default=False
    )
    join_date = fields.DatetimeField(
        auto_now_add=True
    )

    def __str__(self) -> str:
        return f"User {self.id}: {self.username}, {self.email}"
