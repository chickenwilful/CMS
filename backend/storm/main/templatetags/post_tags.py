from django import template
from django.forms import CheckboxInput, TextInput
from storm_user.models import UserProfile

register = template.Library()
