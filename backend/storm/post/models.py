from django.contrib.auth.models import User, Permission
from django.db import models


class Post(models.Model):
    content = models.TextField(max_length=255)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.ForeignKey(User)
    isShared = models.BooleanField()
#    updated_at = models.DateTimeField(auto_now=False)
#    updated_by = models.ForeignKey(User)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        permissions = (
            ('post_create', 'STORM - post_create'),
            ('post_update', 'STORM - post_update'),
            ('post_list', 'STORM - post_list'),
            ('post_delete', 'STORM - post_delete'),
        )


class Comment(models.Model):
    content = models.CharField(max_length=255)
