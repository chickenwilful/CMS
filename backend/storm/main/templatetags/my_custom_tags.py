from django import template
from django.forms import CheckboxInput, TextInput
from storm_user.models import UserProfile

register = template.Library()


@register.filter(name="officalName")
def offcialName(user):
    try:
        userprofile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        pass
    return userprofile.name


@register.filter('klass')
def klass(ob):
    return ob.__class__.__name__


@register.filter(name='is_checkbox')
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__



