from django import template
from django.contrib.auth.models import Group, User
from socialnetwork import utils

register = template.Library()


@register.filter(name='can_list_social')
def can_list_social(user):
    """Helper function to be used as part of a template tag.
    Only CMS Admin can see user list
    """
    return utils.has_socialnetwork_perms(user)
