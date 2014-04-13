"""socialnetwork models module
Defines the only model used by the app.

@author: Muhammad Fazli Bin Rosli
Matriculation Number: N1302335L
"""
from django.db import models

class SocialToken(models.Model):
    """Stores authentication tokens for a social networking service
    """
    site = models.CharField(max_length=255)
    main_token = models.CharField(max_length=255)
    sub_token = models.CharField(max_length=255, null=True)
    expiry_date = models.DateTimeField(null=True)

