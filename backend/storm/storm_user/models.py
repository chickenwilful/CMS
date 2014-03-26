from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

import logging
log = logging.getLogger(__name__)


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    phone_number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

