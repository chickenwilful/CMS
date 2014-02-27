from django.contrib.auth.models import User
from django.db import models


class EmergencySituation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Event(models.Model):
    type = models.ForeignKey(EmergencySituation)
    created_by = models.ForeignKey(User, related_name="creator")
    created_at = models.DateTimeField()
    title = models.CharField(max_length=255, default="title")
    description = models.TextField(null=True)
    related_to = models.ManyToManyField(User, related_name='related')
    caller_name = models.CharField(max_length=255, default="caller_name")
    caller_phone_number = models.CharField(max_length=255, default="caller_phone_number")
    location = models.CharField(max_length=255, default="default location")

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ("event_add", "Can see available event"),
            ("event_edit", "Can change event"),
            ("event_delete", "Can remove event by setting status to closed")
        )


class EventResponse(models.Model):
    content = models.TextField()
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField()



