from django import forms
from tweetfluence.models import User
from datetime import datetime
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        min_length=3,
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),

    )
    password = forms.CharField(
        required=True,
        min_length=4,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if User.objects.filter(username=username).exists() \
        and authenticate(username=username, password=password) is None:
            raise forms.ValidationError('Invalid Credential Combination')

        return cleaned_data

    def fetch_user(self):

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(**self.cleaned_data).save()

        return authenticate(
            username=username,
            password=password
        )



