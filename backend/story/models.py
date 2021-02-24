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
    title = fields.CharField(
        max_length=128
    )
    content = fields.TextField()
    draft = fields.BooleanField(
        default=False
    )
    created_at = fields.DatetimeField(
        auto_now_add=True
    )

    def __str__(self) -> str:
        return f"{self.user} : {self.title}"
