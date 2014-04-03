from django import template
from django.contrib.auth.models import Group, User

register = template.Library()


@register.filter(name='can_list_social')
def can_list_social(user):
    """
    Only CMS Admin can see user list
    """
    return Group.objects.get(name="CMSAdmin") in user.groups.all()
