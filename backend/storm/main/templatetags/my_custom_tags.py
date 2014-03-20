from django import template
from django.forms import CheckboxInput, TextInput

register = template.Library()

@register.filter('klass')
def klass(ob):
    return ob.__class__.__name__

@register.filter(name='is_checkbox')
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__

@register.filter(name='is_textinput')
def is_textinput(field):
    return field.field.widget.__class__.__name__ == TextInput().__class__.__name__


