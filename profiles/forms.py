from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args,**kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email')

    def clean_username(self):
        user = self.cleaned_data['username']
        usernames = [users.user.username for users in Profile.objects.all()]
        if user in usernames:
            self.add_error('username', "Username is already taken")
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        emails = [users.user.email for users in Profile.objects.all()]
        print(email)
        if email != "" and email in emails:
            self.add_error('email', "email is already registered")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'gender', 'city', 'company', )