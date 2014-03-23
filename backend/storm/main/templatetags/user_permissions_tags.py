from django import template

register = template.Library()


@register.filter(name='can_list_user')
def can_list_user(user):
    """
    Only CMS Admin can see user list
    """
    return "CMSAdmin" in user.groups.all()


@register.filter(name='can_retrieve_user')
def can_retrieve_user(user, user_profile):
    """
    CMSAdmin can retrieve profile of every admin
    Users can retrieve their own profile
    """
    return "CMSAdmin" in user.groups.all() or user == user_profile

@register.filter(name='can_create_user')
def can_create_user(user):
    """
    Only CMSAdmin can create user
    """
    return "CMSAdmin" in user.groups.all()


@register.filter(name='can_update_user')
def can_update_user(user, user_profile):
    """
    CMSAdmin can update profile of every admin
    Users can update their own profile
    """
    return "CMSAdmin" in user.groups.all() or user == user_profile


@register.filter(name='can_delete_user')
def can_delete_user(user):
    """
    Only CMSAdminc can delete an user
    """
    return "CMSAdmin" in user.groups.all()


