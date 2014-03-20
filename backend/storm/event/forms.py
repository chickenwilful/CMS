from django import forms
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
from event.models import Event


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, user):
        #userprofile = UserProfile.objects.get(user=user)
        return "%s" % user.email


class EventCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventCreateForm, self).__init__(*args, **kwargs)
    related_to = MyModelChoiceField(queryset=User.objects.filter(groups__name="Rescue Agency"))

    class Meta:
        model = Event
        exclude = ['related_to']


class EventUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventUpdateForm, self).__init__(*args, **kwargs)
        for fieldname in ['related_to']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = Event
