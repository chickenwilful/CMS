from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
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
        self.fields['related_to'] = MyModelChoiceField(queryset=User.objects.filter(groups__name="RescueAgency"), widget=forms.CheckboxSelectMultiple())

    def clean_reporter_phone_number(self):
        #Check that the phone number only contains numeric character
        num = self.cleaned_data.get('reporter_phone_number')
        if num and (not num.isnumeric()):
            raise forms.ValidationError("Phone number must contain only numeric characters")

    class Meta:
        model = Event

#Todo either post_code or address exist


class EventUpdateForm(EventCreateForm):
    pass