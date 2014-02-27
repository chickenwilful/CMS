from django.contrib.auth.models import Group

group = Group.objects.get(name='CMSAdmin')
