from tortoise import fields, models


class Comment(models.Model):
    id = fields.IntField(
        pk=True
    )
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
    content = fields.TextField()
    date = fields.DatetimeField(
        auto_now_add=True
    )

    def __str__(self) -> str:
        return f"User {self.id}: {self.user}, {self.story}"
