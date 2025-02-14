from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Your password must contain at least 8 characters."
        self.fields['password2'].help_text = "Re-enter the same password."

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

        labels = {
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

        help_texts = {
            'username': "Username with letters, digits and @/./+/-/_ only.",
            'password1': "test",
            'password2': "Re-enter the same password.",
        }

        error_messages = {
            'username': {
                'unique': "This username is already taken. Please choose another.",
            },
            'password1': {
                'password_too_short': "Password must be at least 8 characters long.",
                'password_common': "This password is too common, choose another one.",
                'password_entirely_numeric': "Your password cannot be entirely numeric.",
            }
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username
