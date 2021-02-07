from tortoise import fields, models


class Comment(models.Model):
    id = fields.IntField(
        pk=True
    )
    content = fields.TextField()
    user = fields.ForeignKeyField(
        model_name="user.User",
        related_name="user_comments",
        on_delete=fields.SET_NULL
    )
    story = fields.ForeignKeyField(
        model_name="story.Story",
        related_name="story_comments",
        on_delete=fields.SET_NULL
    )
    date = fields.DatetimeField(
        auto_now_add=True
    )

    def __str__(self) -> str:
        return f"User {self.id}: {self.user}, {self.story}"
