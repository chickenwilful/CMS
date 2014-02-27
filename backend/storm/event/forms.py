from django import forms
from event.models import Event


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
