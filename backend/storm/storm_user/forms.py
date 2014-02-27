from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User


class UserLoginForm(forms.ModelForm):
    """
    A form for a user to login
    """
    class Meta:
        model = User
        fields = ('username', 'password')


class UserAddForm(forms.ModelForm):
    """
    A form to create a user. Include all the required fields, plus a repeated password
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'groups')

    def clean_password2(self):
        #Check that the 2 password match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        #save the provided password in hashed format
        user = super(UserAddForm, self).save(commit=False)
        user.set_password(self.clean_data['password1'])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    """
    A form for edit profile user. Included all the fields on the user, but replaces the password field
    with password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password(self):
        """
        Regardless of what the user provide, return the initial value
        This is done here, rather than on the field, because the field
        does not have access to the initial value
        """
        return self.initial['password']