from django.contrib.auth.models import User, Permission
from django.db import models
from event.models import EmergencySituation


class Post(models.Model):
    type = models.ForeignKey(EmergencySituation)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=255)
    imageLink = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.ForeignKey(User)
    isPublished = models.BooleanField(default=True)

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
