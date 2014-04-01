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
        self.fields['related_to'].help_text = None
        self.fields['reporter_phone_number'].widget.attrs['type'] = "number"
    related_to = MyModelChoiceField(queryset=User.objects.filter(groups__name="RescueAgency"),
                                    widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Event
        exclude = ['related_to']



class EventUpdateForm(EventCreateForm):
    class Meta:
        model = Event

    def save(self, commit=True):
        event = super(EventCreateForm, self).save(commit=False)
        event.save()
        return event
