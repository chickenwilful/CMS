from django.contrib.auth.models import User, Permission
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=255)
    imageLink = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.ForeignKey(User, editable=False)
    isShared = models.BooleanField(default=False)

#    updated_at = models.DateTimeField(auto_now=False)
#    updated_by = models.ForeignKey(User)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        permissions = (
            ('post_create', 'STORM - post create'),
            ('post_update', 'STORM - post update'),
            ('post_list', 'STORM - post list'),
            ('post_delete', 'STORM - post delete'),
            ('post_retrieve', 'STORM - post retrieve'),
        )
