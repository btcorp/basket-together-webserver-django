from django import forms
from accounts.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'device_type', 'user_image', )


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password', )