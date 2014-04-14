from django import forms
from django.contrib.auth.models import User, Group
from storm_user.models import UserProfile


class UserLoginForm(forms.ModelForm):
    """
    A form for a user to login
    """
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for fieldname in ['username']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username',)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class UserCreateForm(forms.ModelForm):
    """
    A form to create a user. Include all the required fields, plus a repeated password
    """
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'groups']:
            self.fields[fieldname].help_text = None
        # self.fields['groups'].widget = forms.CheckboxSelectMultiple(choices=self.fields['groups'].choices)

    name = forms.CharField(label="Name", widget=forms.TextInput)
    phone_number = forms.CharField(label="Phone number", widget=forms.TextInput)

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'groups')

    def clean_password2(self):
        #Check that the 2 password match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2

    def clean_phone_number(self):
        #Check that the phone number only contains numeric character
        num = self.cleaned_data.get('phone_number')
        if num and (not num.isnumeric()):
            raise forms.ValidationError("Phone number must contain only numeric characters")
        return num

    def save(self, commit=True):
        #save the provided password in hashed format
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
    A form for edit profile user. Included all the fields on the user, but replaces the password field
    with password hash display field.
    """
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
        self.fields['username'].widget.attrs["readonly"] = "readonly"
        self.fields['password'].widget.attrs["readonly"] = "readonly"
        try:
            userprofile = UserProfile.objects.get(user=self.instance)
            self.fields['name'].initial = userprofile.name
            self.fields['phone_number'].initial = userprofile.phone_number
        except UserProfile.DoesNotExist:
            pass

    name = forms.CharField(label="Name", widget=forms.TextInput, required=True)
    phone_number = forms.CharField(label="Phone number", widget=forms.TextInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'groups', 'email', 'name', 'phone_number', 'password']

    def clean_phone_number(self):
        #Check that the phone number only contains numeric character
        num = self.cleaned_data.get('phone_number')
        if num and (not num.isnumeric()):
            raise forms.ValidationError("Phone number must contain only numeric characters")
        return num

    def clean_password(self):
        """
        Regardless of what the user provide, return the initial value
        This is done here, rather than on the field, because the field
        does not have access to the initial value
        """
        return self.instance.password

