from django.contrib.auth.models import User
user = User.objects.get(username="yen")
user.set_password("yen")