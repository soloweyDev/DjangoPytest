from django.contrib.auth.forms import UserCreationForm
from django.forms import forms
from .models import User


class RegisterForm(UserCreationForm):
    image = forms.FileField(label="image")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'image']
