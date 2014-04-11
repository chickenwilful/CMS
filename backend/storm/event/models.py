from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class EmergencySituation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Event(models.Model):
    type = models.ForeignKey(EmergencySituation)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name="creator", editable=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    related_to = models.ManyToManyField(User, related_name='related_to')
    reporter_name = models.CharField(max_length=255, null=True, blank=True)
    reporter_phone_number = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(
        max_length=255, null=True, blank=True,
        validators=[RegexValidator(
            regex='^\d{6}$', message='Invalid Singapore Postal Code', code='Invalid number')
        ]
    )
    #Todo postal_code unique
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ("event_create", "STORM - event create"),
            ("event_retrieve", "STORM - event retrieve"),
            ("event_update", "STORM - event update"),
            ("event_delete", "STORM - event delete"),
            ("event_list", "STORM - event list"),
        )




