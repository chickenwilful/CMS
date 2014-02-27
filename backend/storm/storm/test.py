from django.contrib.auth.models import User

user = User.objects.get(pk=3)
user.related_set.all()