from django import template
from django.contrib.auth.models import User, Group

register = template.Library()


@register.filter(name='can_list_event')
def can_list_event(user):
    return "event.event_list" in user.get_all_permissions()


@register.filter(name='can_retrieve_event')
def can_retrieve_event(user, event):
    return Group.objects.get(name="CMSAdmin") in user.groups.all() \
        or ("event.event_retrieve" in user.get_all_permissions() and user in event.related_to.all())


@register.filter(name='can_create_event')
def can_create_event(user):
    return "event.event_create" in user.get_all_permissions()


@register.filter(name='can_update_event')
def can_update_event(user, event):
    ans = "event.event_create" in user.get_all_permissions()
    return ans and (user == event.created_by or (Group.objects.get(name="CMSAdmin") in user.groups.all()))


@register.filter(name='can_delete_event')
def can_delete_event(user, event):
    ans = "event.event_delete" in user.get_all_permissions()
    return ans and (user == event.created_by or (Group.objects.get(name="CMSAdmin") in user.groups.all()))


