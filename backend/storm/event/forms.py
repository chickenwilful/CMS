from django import forms
from django.contrib.auth.models import User
from django.forms import ModelMultipleChoiceField
from event.models import Event
from storm_user.models import UserProfile


class MyModelChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, user):
        userprofile = UserProfile.objects.get(user=user)
        return "%s" % userprofile.name


class EventCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventCreateForm, self).__init__(*args, **kwargs)
        for fieldname in ['related_to']:
            self.fields[fieldname].help_text = None
    related_to = MyModelChoiceField(queryset=User.objects.filter(groups__name="RescueAgency"))

    class Meta:
        model = Event
        exclude = ['related_to']

    def save(self, commit=True):
        event = super(EventCreateForm, self).save(commit=False)
        event.save()
        event.related_to = self.cleaned_data.get('related_to')
        event.save()
        return event


class EventUpdateForm(EventCreateForm):
    class Meta:
        model = Event

    def save(self, commit=True):
        event = super(EventCreateForm, self).save(commit=False)
        event.save()
        return event
