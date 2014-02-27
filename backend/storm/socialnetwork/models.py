from django.db import models


class SocialToken(models.Model):
    site = models.CharField(max_length=255)
    main_token = models.CharField(max_length=255)
    sub_token = models.CharField(max_length=255, null=True)
    expiry_date = models.DateTimeField(null=True)

