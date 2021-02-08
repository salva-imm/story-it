from tortoise import fields, models


class Comment(models.Model):
    id = fields.IntField(
        pk=True
    )
    content = fields.TextField()
    user = fields.ForeignKeyField(
        model_name="models.User",
        related_name="user_comments",
        on_delete=fields.SET_NULL,
        null=True,
    )
    story = fields.ForeignKeyField(
        model_name="models.Story",
        related_name="story_comments",
        on_delete=fields.SET_NULL,
        null=True,
    )
    date = fields.DatetimeField(
        auto_now_add=True
    )

    def __str__(self) -> str:
        return f"User {self.id}: {self.user}, {self.story}"
