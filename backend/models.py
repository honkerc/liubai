from tortoise import fields
from tortoise.models import Model
import uuid


class User(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    username = fields.CharField(max_length=50, unique=True, index=True)
    password_hash = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"

    def __str__(self):
        return self.username


class Article(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    author = fields.ForeignKeyField("models.User", related_name="articles")
    title = fields.CharField(max_length=200, unique=True, index=True)
    content = fields.TextField(default="")
    topic = fields.CharField(max_length=100, default="")  # 话题
    is_published = fields.BooleanField(default=True)  # True=已发布, False=草稿
    is_pinned = fields.BooleanField(default=False)  # 置顶
    views = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "articles"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or self.content[:50]
